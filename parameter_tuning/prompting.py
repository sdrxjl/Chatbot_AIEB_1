import re
from typing import List, Tuple

def history_pairs_to_text(pairs: List[Tuple[str, str]], turns: int) -> str:
    if turns <= 0:
        return ""
    trimmed = pairs[-turns:]
    out = ""
    for u, a in trimmed:
        out += f"User: {u}\nAssistant: {a}\n\n"
    return out.strip()

def build_prompt(question: str, context_text: str, history_text: str, use_history: bool) -> str:
    history_block = ""
    if use_history and history_text.strip():
        history_block = f"\n\nChat History:\n{history_text.strip()}\n"

    return f"""
You are a precise, helpful assistant that answers questions based on the provided documents.
Answer the user's question using only information from the documents. Scale the depth of your answer to the complexity of the question — concise for simple questions, thorough for complex ones. If the documents only partially answer the question, provide what you can and clearly note what is not covered.
Structure your response for readability. For example, use paragraphs for explanations, bullet points for lists or comparisons, and headers only when the answer has multiple parts.
Cite every factual claim inline using bracket numbers like [1], [2]. If multiple sources support a claim, cite all of them. If the answer cannot be found in the documents at all, respond: “I don't have enough information to answer this question.


{history_block}

Context:
{context_text}

Question:
{question}

Answer:
""".strip()

'''
def extract_citation_indices(answer_text: str):
    nums = re.findall(r"\[(\d+)\]", answer_text)
    return sorted({int(n) for n in nums})
'''

def extract_citation_indices(answer_text: str) -> list[int]:
    # find anything inside [...]
    groups = re.findall(r"\[([0-9,\s\-]+)\]", answer_text)
    out = set()

    for g in groups:
        parts = [p.strip() for p in g.split(",") if p.strip()]
        for p in parts:
            if "-" in p:
                a, b = p.split("-", 1)
                if a.strip().isdigit() and b.strip().isdigit():
                    lo, hi = int(a), int(b)
                    for x in range(min(lo, hi), max(lo, hi) + 1):
                        out.add(x)
            else:
                if p.isdigit():
                    out.add(int(p))

    return sorted(out)