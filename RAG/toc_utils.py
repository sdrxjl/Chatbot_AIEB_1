import re
from typing import List, Tuple

def build_toc_map_from_loaded_pages(loaded_pages) -> List[Tuple[int, str]]:
    first_pages_text = "\n".join([p.page_content for p in loaded_pages[:8]])
    pattern = re.compile(r"(?im)^\s*(Item\s+\d+[A-Z]?\.\s+.+?)\s+(\d+)\s*$")

    entries = []
    for m in pattern.finditer(first_pages_text):
        title = re.sub(r"\s+", " ", m.group(1)).strip()
        start_page = int(m.group(2))
        entries.append((start_page, title))

    seen = set()
    deduped = []
    for p, t in entries:
        key = (p, t.lower())
        if key not in seen:
            seen.add(key)
            deduped.append((p, t))

    deduped.sort(key=lambda x: x[0])
    return deduped

def lookup_section_by_page(toc_entries: List[Tuple[int, str]], pdf_page_0based: int) -> str:
    page_1based = pdf_page_0based + 1
    if not toc_entries:
        return "Unknown Section"
    current = "Unknown Section"
    for start_page, title in toc_entries:
        if page_1based >= start_page:
            current = title
        else:
            break
    return current