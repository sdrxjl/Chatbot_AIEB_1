"""
Batch QA runner (fixed paths + inline API key)
------------------------------------------------
- Reads questions from ./question/questions.csv
- Uses PDFs from ./files (folder)
- Runs retrieval + Gemini generation
- Saves ./question/results.csv with added columns: output, citations

INPUT CSV must include at least:
- question
- company

Citations column contains a JSON string list of cited chunks:
  [{"idx": 1, "source": "...pdf", "page": 12, "section": "Item 7. ..."}, ...]

IMPORTANT SECURITY NOTE:
- This file lets you put an API key directly in code. Avoid committing it to Git.
"""

import os
import re
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Reuse your project modules (uploaded in this workspace)
from app_config import (
    CACHE_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MAX_CHUNKS_PER_FILE,
    TOP_K_PER_FILE,
    MAX_CONTEXT_CHUNKS,
    choice
)
from cache_utils import cache_path_for, has_cached_index, save_manifest
from toc_utils import build_toc_map_from_loaded_pages, lookup_section_by_page
from embeddings_utils import build_embeddings, build_llm
from retrieval_0 import retrieve_docs_for_files, build_context_text
from prompting import build_prompt, extract_citation_indices




# =========================
# EDIT THESE 3 CONSTANTS
# =========================
PDF_DIR = Path("./files")                       # folder containing PDFs
INPUT_CSV = Path("./question/questions.csv")    # input CSV file
OUTPUT_CSV = Path(f"./question/results_{choice.lower()}.csv")     # output CSV file

# Put your key here (or leave empty and set GOOGLE_API_KEY in environment)
GOOGLE_API_KEY = "GOOGLE_API_KEY"
# =========================


# ----------------------------
# Helpers
# ----------------------------

def _norm_company(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").strip().lower()).strip()

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def select_company_files(
    pdf_dir: Path,
    company: str,
    company_to_keywords: Dict[str, List[str]] | None = None,
) -> List[Path]:
    """
    Default heuristic: pick PDFs whose filename contains the company token (case-insensitive).
    Optionally provide company_to_keywords for tighter control.
    """
    pdfs = sorted(pdf_dir.glob("*.pdf"))
    if not pdfs:
        return []

    c_norm = _norm_company(company)
    if not c_norm:
        return []

    keywords: List[str] = []
    if company_to_keywords:
        if company in company_to_keywords:
            keywords = company_to_keywords[company]
        else:
            for k, v in company_to_keywords.items():
                if _norm_company(k) == c_norm:
                    keywords = v
                    break

    keys = [_norm_company(k) for k in keywords if _norm_company(k)] if keywords else [c_norm]

    out: List[Path] = []
    for p in pdfs:
        name = _norm_company(p.name)
        if any(k in name for k in keys):
            out.append(p)
    return out


def build_or_load_indexes_from_paths(
    pdf_paths: List[Path],
    embeddings,
    cache_root: Path,
    index_by_file: Dict[str, FAISS],
) -> None:
    """
    Builds/loads FAISS indexes per PDF and caches them in CACHE_DIR.
    """
    item_heading_pattern = re.compile(r"(Item\s+\d+[A-Z]?\.\s+[^\n]+)", re.IGNORECASE)

    for path in pdf_paths:
        fn = path.name
        if fn in index_by_file:
            continue

        file_hash = _sha256_file(path)
        cp = cache_path_for(cache_root, file_hash)

        if has_cached_index(cp):
            try:
                vs = FAISS.load_local(str(cp), embeddings, allow_dangerous_deserialization=True)
                index_by_file[fn] = vs
                continue
            except Exception:
                pass  # fall back to rebuild

        pages = PyPDFLoader(str(path)).load()

        toc_entries = build_toc_map_from_loaded_pages(pages)
        for d in pages:
            d.metadata["source"] = fn
            d.metadata["page"] = d.metadata.get("page", 0)
            d.metadata["section"] = lookup_section_by_page(toc_entries, d.metadata["page"])

        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunks = splitter.split_documents(pages)

        for c in chunks:
            m = item_heading_pattern.search(c.page_content)
            if m:
                c.metadata["section"] = re.sub(r"\s+", " ", m.group(1)).strip()

        if len(chunks) > MAX_CHUNKS_PER_FILE:
            chunks = chunks[:MAX_CHUNKS_PER_FILE]

        vs = FAISS.from_documents(chunks, embeddings)
        index_by_file[fn] = vs

        cp.mkdir(parents=True, exist_ok=True)
        vs.save_local(str(cp))
        save_manifest(cp, {
            "filename": fn,
            "sha256": file_hash,
            "chunks": len(chunks),
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        })


def build_citations_payload(retrieved_docs, cited_indices: List[int]) -> List[Dict[str, Any]]:
    """
    Compact citations for ONLY cited chunk indices. (No evidence text.)
    """
    out: List[Dict[str, Any]] = []
    cited_set = set(cited_indices or [])
    if not cited_set:
        return out

    for i, d in enumerate(retrieved_docs, 1):
        if i not in cited_set:
            continue
        out.append({
            "idx": i,
            "source": d.metadata.get("source", "Unknown File"),
            "page": int(d.metadata.get("page", 0)) + 1,  # 1-based
            "section": d.metadata.get("section", "Unknown Section"),
        })
    return out


def main():
    # --- API Key handling ---
    # If you set GOOGLE_API_KEY above, use it; otherwise fall back to environment.
    if GOOGLE_API_KEY:
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY  # always set if provided

    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Put it into GOOGLE_API_KEY constant in this file, "
            "or set it as an environment variable before running."
        )
    # --- Validate paths ---
    if not PDF_DIR.exists():
        raise FileNotFoundError(f"PDF folder not found: {PDF_DIR.resolve()}")
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Input CSV not found: {INPUT_CSV.resolve()}")

    # Load CSV
    df = pd.read_csv(INPUT_CSV)
    if "question" not in df.columns or "company" not in df.columns:
        raise ValueError("Input CSV must contain columns: 'question' and 'company'.")

    # Models
    embeddings = build_embeddings()
    llm = build_llm()

    # Index cache
    index_by_file: Dict[str, FAISS] = {}

    outputs: List[str] = []
    citations_col: List[str] = []

    for row_idx, row in df.iterrows():
        question = str(row.get("question", "")).strip()
        company = str(row.get("company", "")).strip()

        if not question:
            outputs.append("")
            citations_col.append("[]")
            continue

        '''
        company_files = select_company_files(
        PDF_DIR, company,
        company_to_keywords={
            "Amazon": ["amazon", "amzn", "aws"],
            "Alphabet": ["alphabet", "google", "goog", "googl"],
            "Microsoft": ["microsoft", "msft"],
        })'''
        if company.lower() in ["multiple", "multiple/general"]:
            # use all PDFs
            company_files = list(PDF_DIR.glob("*.pdf"))
        else:
            company_files = select_company_files(
                PDF_DIR,
                company,
                company_to_keywords={
                    "Amazon": ["amazon", "amzn", "aws"],
                    "Alphabet": ["alphabet", "google", "goog", "googl"],
                    "Microsoft": ["microsoft", "msft"],
                },
            )


        if not company_files:
            outputs.append(
                f"I don't have enough information to answer this question. "
                f"(No PDFs matched company '{company}'.)"
            )
            citations_col.append("[]")
            continue

        build_or_load_indexes_from_paths(
            pdf_paths=company_files,
            embeddings=embeddings,
            cache_root=CACHE_DIR,
            index_by_file=index_by_file,
        )

        effective_files = [p.name for p in company_files]

        retrieved_docs = retrieve_docs_for_files(
            index_by_file=index_by_file,
            files=effective_files,
            question=question,
            top_k_per_file=TOP_K_PER_FILE,
            max_context_chunks=MAX_CONTEXT_CHUNKS,
        )

        context_text = build_context_text(retrieved_docs)
        prompt = build_prompt(question=question, context_text=context_text, history_text="", use_history=False)

        resp = llm.invoke(prompt)
        #answer_text = getattr(resp, "content", str(resp)).strip()
        time.sleep(4)

        raw_content = getattr(resp, "content", "")
        print(f"Row {row_idx}: raw response = {repr(getattr(resp, 'content', None))}", flush=True)
        answer_text = (raw_content if raw_content is not None else "").strip()

        if not answer_text:
            answer_text = "I don't have enough information to answer this question."

        cited_indices = extract_citation_indices(answer_text)
        citations_payload = build_citations_payload(retrieved_docs, cited_indices)

        outputs.append(answer_text)
        citations_col.append(json.dumps(citations_payload, ensure_ascii=False))

        if (row_idx + 1) % 1 == 0:
        
            print(f"Processed {row_idx + 1}/{len(df)}")

    df_out = pd.DataFrame({
        "output": outputs,
        "citations": citations_col
    })

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    print("Writing to:", OUTPUT_CSV.resolve(), flush=True)
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    


if __name__ == "__main__":
    main()
