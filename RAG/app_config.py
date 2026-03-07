from pathlib import Path

MAX_OUTPUT_TOKENS = 2048

# =============================
# PATHS
# =============================
CACHE_DIR = Path(".rag_cache/faiss")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# =============================
# CHUNKING / RETRIEVAL
# =============================
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 140
MAX_CHUNKS_PER_FILE = 1600

TOP_K_PER_FILE = 7
MAX_CONTEXT_CHUNKS = 20

# =============================
# UI / OUTPUT
# =============================
STREAM_DELAY = 0.008
EVIDENCE_EXCERPT_CHARS = 1200



MMR_FETCH_K_MULT = 610     # fetch_k = max(20, TOP_K_PER_FILE * MMR_FETCH_K_MULT)
MMR_LAMBDA_MULT = 0.5 
MMR_FETCH_K_MIN = 80 

