import os
import re
import time
import tempfile
from typing import List, Dict

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from app_config import CHUNK_SIZE, CHUNK_OVERLAP, MAX_CHUNKS_PER_FILE
from cache_utils import sha256_bytes, cache_path_for, has_cached_index, save_manifest
from toc_utils import build_toc_map_from_loaded_pages, lookup_section_by_page

def build_or_load_indexes(
    uploaded_files,
    embeddings,
    cache_root,
    index_by_file: Dict[str, FAISS],
):
    progress = st.progress(0, text="Preparing indexes...")
    total = len(uploaded_files)
    ready = 0

    with st.spinner("Checking cache / building indexes..."):
        with tempfile.TemporaryDirectory() as temp_dir:
            for f in uploaded_files:
                b = f.getvalue()
                h = sha256_bytes(b)
                cp = cache_path_for(cache_root, h)

                # already in memory
                if f.name in index_by_file:
                    ready += 1
                    progress.progress(int(ready / total * 100), text=f"Ready: {ready}/{total}")
                    continue

                # load from disk
                if has_cached_index(cp):
                    try:
                        vs = FAISS.load_local(str(cp), embeddings, allow_dangerous_deserialization=True)
                        index_by_file[f.name] = vs
                        ready += 1
                        progress.progress(int(ready / total * 100), text=f"Loaded cache: {ready}/{total}")
                        continue
                    except Exception as e:
                        st.warning(f"Cache load failed for {f.name}, rebuilding. Reason: {e}")

                # build fresh
                try:
                    temp_path = os.path.join(temp_dir, f.name)
                    with open(temp_path, "wb") as out:
                        out.write(b)

                    pages = PyPDFLoader(temp_path).load()

                    toc_entries = build_toc_map_from_loaded_pages(pages)
                    for d in pages:
                        d.metadata["source"] = f.name
                        d.metadata["page"] = d.metadata.get("page", 0)
                        d.metadata["section"] = lookup_section_by_page(toc_entries, d.metadata["page"])

                    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
                    chunks = splitter.split_documents(pages)

                    # override section if chunk contains Item heading
                    item_heading_pattern = re.compile(r"(Item\s+\d+[A-Z]?\.\s+[^\n]+)", re.IGNORECASE)
                    for c in chunks:
                        m = item_heading_pattern.search(c.page_content)
                        if m:
                            c.metadata["section"] = re.sub(r"\s+", " ", m.group(1)).strip()

                    if len(chunks) > MAX_CHUNKS_PER_FILE:
                        chunks = chunks[:MAX_CHUNKS_PER_FILE]

                    vs = FAISS.from_documents(chunks, embeddings)
                    index_by_file[f.name] = vs

                    cp.mkdir(parents=True, exist_ok=True)
                    vs.save_local(str(cp))
                    save_manifest(cp, {
                        "filename": f.name,
                        "sha256": h,
                        "chunks": len(chunks),
                        "chunk_size": CHUNK_SIZE,
                        "chunk_overlap": CHUNK_OVERLAP,
                        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    })

                    ready += 1
                    progress.progress(int(ready / total * 100), text=f"Built index: {ready}/{total}")

                except Exception as e:
                    st.error(f"Failed to build index for {f.name}.\n\nError: {e}")
                    st.stop()

    progress.progress(100, text="Indexes ready")