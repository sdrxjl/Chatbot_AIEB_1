from typing import List, Tuple, Dict
from langchain_core.documents import Document

from app_config import MMR_FETCH_K_MULT, MMR_LAMBDA_MULT, MMR_FETCH_K_MIN


#


def scope_key(files: List[str]) -> str:
    return "|".join(sorted(files))

def retrieve_docs_for_files(index_by_file: Dict[str, object], files: List[str], question: str,
                            top_k_per_file: int, max_context_chunks: int) -> List[Document]:
    retrieved_docs: List[Document] = []

    fetch_k = max(MMR_FETCH_K_MIN, top_k_per_file * MMR_FETCH_K_MULT)
    for fn in files:
        retriever = index_by_file[fn].as_retriever(
            search_type="mmr",
            search_kwargs={"k": top_k_per_file, "fetch_k": fetch_k, "lambda_mult": MMR_LAMBDA_MULT}
        )
        retrieved_docs.extend(retriever.get_relevant_documents(question))
        

    # de-dup
    dedup = {}
    for d in retrieved_docs:
        src = d.metadata.get("source", "Unknown File")
        page0 = d.metadata.get("page", 0)
        section = d.metadata.get("section", "Unknown Section")
        key = (src, page0, section, hash(d.page_content[:500]))
        dedup[key] = d

    return list(dedup.values())[:max_context_chunks]

def build_context_text(retrieved_docs: List[Document]) -> str:
    blocks = []
    for i, d in enumerate(retrieved_docs, 1):
        src = d.metadata.get("source", "Unknown File")
        page0 = d.metadata.get("page", 0)
        section = d.metadata.get("section", "Unknown Section")
        blocks.append(
            f"[{i}] Source: {src} | Page: {page0 + 1} | Section: {section}\n{d.page_content}"
        )
    return "\n\n".join(blocks)