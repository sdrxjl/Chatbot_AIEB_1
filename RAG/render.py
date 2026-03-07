import re
import time
from typing import List, Set
from langchain_core.documents import Document


def md_formatting(text: str) -> str:
    # Escape $ when it looks like currency ($ followed by a number)
    text = text.replace("`", "")
    text = text.replace("_", r"\_")
    text = re.sub(r'(?<!\\)\$(?=\s*\d)', r'\\$', text)
    return text

def stream_markdown_preserve_whitespace(placeholder, text: str, delay: float) -> str:
    parts = re.findall(r"\s+|[^\s]+", text)
    acc = ""
    for p in parts:
        acc += p
        placeholder.markdown(md_formatting(acc))
        time.sleep(delay)
    return acc
'''
def stream_text_preserve_whitespace(placeholder, text: str, delay: float) -> str:
    parts = re.findall(r"\s+|[^\s]+", text)
    acc = ""
    for p in parts:
        acc += p
        placeholder.text(acc)   # <-- key change
        time.sleep(delay)
    return acc'''

def normalize_excerpt(text: str, n: int) -> str:
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    if len(text) <= n:
        return text
    return text[:n].rstrip() + " …"

'''def build_sources_md(retrieved_docs: List[Document]) -> str:
    if not retrieved_docs:
        return ""
    md = "\n\n---\n### 📚 Sources\n\n"
    for i, d in enumerate(retrieved_docs, 1):
        
        src = d.metadata.get("source", "Unknown File")
        page0 = d.metadata.get("page", 0)
        section = d.metadata.get("section", "Unknown Section")
        md += (
            f"[{i}] **{src}**  \n"
            f"Page: {page0 + 1}  \n"
            f"Section: {section}\n\n"
        )
    return md'''

def build_evidence_md(retrieved_docs: List[Document], cited_set: Set[int], excerpt_chars: int):
    evidence_blocks_all = []
    evidence_blocks_cited = []

    for i, d in enumerate(retrieved_docs, 1):
        src = d.metadata.get("source", "Unknown File")
        page0 = d.metadata.get("page", 0)
        section = d.metadata.get("section", "Unknown Section")
        chunk_text = d.page_content.strip()
        excerpt = normalize_excerpt(chunk_text, excerpt_chars)

        block = (
            f"#### [{i}] {src} — Page {page0 + 1} — {section}\n"
            f"**Excerpt:**\n\n"
            f"> {excerpt.replace(chr(10), chr(10) + '> ')}\n\n"
            f"<details><summary>Show full chunk</summary>\n\n"
            f"{chunk_text}\n\n"
            f"</details>\n"
        )

        evidence_blocks_all.append(block)
        if i in cited_set:
            evidence_blocks_cited.append(block)

    evidence_all_md = "\n\n".join(evidence_blocks_all) if evidence_blocks_all else "No evidence chunks to display."
    evidence_cited_md = "\n\n".join(evidence_blocks_cited) if evidence_blocks_cited else "No cited evidence chunks found in the answer."
    return evidence_all_md, evidence_cited_md