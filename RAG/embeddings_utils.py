import time
import random
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from app_config import MAX_OUTPUT_TOKENS

class RetryEmbeddings(Embeddings):
    def __init__(self, base: Embeddings, max_retries: int = 8, base_sleep: float = 2.0):
        self.base = base
        self.max_retries = max_retries
        self.base_sleep = base_sleep

    def embed_documents(self, texts):
        last_err = None
        for i in range(self.max_retries):
            try:
                return self.base.embed_documents(texts)
            except Exception as e:
                last_err = e
                time.sleep(self.base_sleep * (2 ** i) + random.uniform(0, 1.0))
        raise last_err

    def embed_query(self, text):
        last_err = None
        for i in range(self.max_retries):
            try:
                return self.base.embed_query(text)
            except Exception as e:
                last_err = e
                time.sleep(self.base_sleep * (2 ** i) + random.uniform(0, 1.0))
        raise last_err

def build_embeddings():
    base = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return RetryEmbeddings(base, max_retries=8, base_sleep=2.0)

def build_llm():
    return ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.5,max_output_tokens=MAX_OUTPUT_TOKENS)