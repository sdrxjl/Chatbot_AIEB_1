import os
import json
import tempfile
from pathlib import Path

import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

PDF_DIR = Path("./files")
INPUT_CSV = Path("./question/questions.csv")
OUTPUT_CSV = Path("./question/results_prof_baseline.csv")

GOOGLE_API_KEY = "GOOGLE API KEY"

persona = '''
You are a helpful assistant that answers questions based on the provided documents.
Answer the question with detailed information from the documents. If the answer is not in the documents,
say "I don't have enough information to answer this question." Cite specific parts of the documents when possible.
Consider the chat history for context when answering, but prioritize information from the documents.
'''

template = """
{persona}

Chat History:
<history>
{chat_history}
</history>

Given the context information and not prior knowledge, answer the following question:
Question: {user_input}
"""

def build_vector_store(pdf_dir: Path, embeddings):
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {pdf_dir.resolve()}")

    documents = []

    with tempfile.TemporaryDirectory() as temp_dir:
        for pdf_path in pdf_files:
            temp_file_path = Path(temp_dir) / pdf_path.name
            temp_file_path.write_bytes(pdf_path.read_bytes())

            loader = PyPDFLoader(str(temp_file_path))
            loaded_docs = loader.load()

            for d in loaded_docs:
                d.metadata["source"] = pdf_path.name

            documents.extend(loaded_docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    return FAISS.from_documents(docs, embeddings)

def build_citations(source_documents):
    citations = []
    for i, doc in enumerate(source_documents, start=1):
        page_val = doc.metadata.get("page", "unknown")
        if isinstance(page_val, int):
            page_val = page_val + 1
        citations.append({
            "idx": i,
            "source": doc.metadata.get("source", "Unknown File"),
            "page": page_val,
        })
    return citations

def main():
    if GOOGLE_API_KEY and GOOGLE_API_KEY != "YOUR_GOOGLE_API_KEY":
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("Set GOOGLE_API_KEY in the script or in your environment.")

    if not PDF_DIR.exists():
        raise FileNotFoundError(f"PDF folder not found: {PDF_DIR.resolve()}")

    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Input CSV not found: {INPUT_CSV.resolve()}")

    df = pd.read_csv(INPUT_CSV)
    if "question" not in df.columns:
        raise ValueError("Input CSV must contain a 'question' column.")

    print("Building embeddings model...", flush=True)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    print("Building LLM...", flush=True)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

    print("Processing PDFs and building FAISS vector store...", flush=True)
    vector_store = build_vector_store(PDF_DIR, embeddings)

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.7}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        verbose=False,
        chain_type_kwargs={"verbose": False}
    )

    outputs = []
    citations_col = []

    for row_idx, row in df.iterrows():
        question = str(row.get("question", "")).strip()

        if not question:
            outputs.append("")
            citations_col.append("[]")
            continue

        print(f"Processed {row_idx + 1}/{len(df)}", flush=True)

        response = qa_chain.invoke({
            "query": template.format(
                persona=persona,
                user_input=question,
                chat_history=""
            ),
        })

        response_text = response.get("result", "").strip()
        source_documents = response.get("source_documents", [])

        outputs.append(response_text)
        citations_col.append(json.dumps(build_citations(source_documents), ensure_ascii=False))

    df_out = pd.DataFrame({
        "output": outputs,
        "citations": citations_col
    })

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing to: {OUTPUT_CSV.resolve()}", flush=True)
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print("Done.", flush=True)

if __name__ == "__main__":
    main()