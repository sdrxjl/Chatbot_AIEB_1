# Financial 10-K RAG Chatbot

This project implements a Retrieval-Augmented Generation (RAG) chatbot to analyze and answer questions about the 10-K filings of Alphabet, Amazon, and Microsoft.

---

## Environment Setup

Install the required packages using the following commands.

### Conda packages

```bash
conda install -c conda-forge -y streamlit faiss-cpu pdf2image pytesseract pillow
```

### Pip packages

```bash
pip install "langchain==0.2.16" "langchain-community==0.2.16" "langchain-core==0.2.43" "langchain-text-splitters==0.2.4" "langchain-ollama==0.1.3" "ollama>=0.3.0,<1" "pypdf>=3.15.1,<5" "langchain-openai==0.1.17" "openai>=1.32.0,<2" "langchain-google-genai==1.0.10" "google-generativeai>=0.7.0,<0.8.0"
```

---

## Running the Application

Launch the chatbot with:

```bash
streamlit run RAG/main.py
```

---

## Technical Notes

Additional implementation details and design discussion can be found in:

technotes.pdf

---

## Teamwork Contribution and Workflow

We separated the work into three groups: **Group A**, **Group B**, and **Group C**.

### Group A — Question Bank Creation

Qi Kan (@kkkqqq1116)  
Emanuel Telles Chaves  

### Group B — RAG Pipeline, Evaluation, and Persona

Yixuan Han (@sdrxjl)  
Tianjin Duan (@TianjinDuan01)  
Calis Nguyen (@cnguye95)

### Group C — Presentation Slides

Xiaojia Wang (@wangxiaojia31)  
Zihan Wang

---

## Process Flow

Group A → Develops question bank → Group B  

Group B → Builds and evaluates the RAG pipeline and documents findings → Group C  

Group C → Designs slides based on outputs from Group A and Group B for the final presentation
