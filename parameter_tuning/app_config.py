from pathlib import Path


# =============================
# PATHS
# =============================
CACHE_DIR = Path(".rag_cache/faiss")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


'''
MAX_OUTPUT_TOKENS = 2048
# =============================
# CHUNKING / RETRIEVAL
# =============================
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
MAX_CHUNKS_PER_FILE = 1500

TOP_K_PER_FILE = 6
MAX_CONTEXT_CHUNKS = 18

# =============================
# UI / OUTPUT
# =============================
STREAM_DELAY = 0.008
EVIDENCE_EXCERPT_CHARS = 1200



MMR_FETCH_K_MULT = 6      # fetch_k = max(20, TOP_K_PER_FILE * MMR_FETCH_K_MULT)
MMR_LAMBDA_MULT = 0.5 
MMR_FETCH_K_MIN = 40  

#if too off topic: raise MMR_LAMBDA_MULT (try 0.6) or lower RETRIEVE_K_MULT
#if too repetitive lower MMR_LAMBDA_MULT

# Dedup tuning
DEDUP_SIM_THRESHOLD = 0.94 #if still has repeats increase this
DEDUP_MAX_COMPARE = 200 

RETRIEVE_K_MULT = 2 #final k per file'''


choice = "S"   # change only this: A-S
choice = choice.upper()

CONFIGS = {
    "A": {
        "MAX_OUTPUT_TOKENS": 1024,
        "CHUNK_SIZE": 1800,
        "CHUNK_OVERLAP": 120,
        "MAX_CHUNKS_PER_FILE": 250,
        "TOP_K_PER_FILE": 2,
        "MAX_CONTEXT_CHUNKS": 4,
        "MMR_FETCH_K_MULT": 4,
        "MMR_FETCH_K_MIN": 20,
        "MMR_LAMBDA_MULT": 0.65,
        "DEDUP_SIM_THRESHOLD": 0.93,
        "DEDUP_MAX_COMPARE": 120,
        "RETRIEVE_K_MULT": 1,
        "EVIDENCE_EXCERPT_CHARS": 800,
    },
    "B": {
        "MAX_OUTPUT_TOKENS": 1536,
        "CHUNK_SIZE": 1400,
        "CHUNK_OVERLAP": 150,
        "MAX_CHUNKS_PER_FILE": 600,
        "TOP_K_PER_FILE": 3,
        "MAX_CONTEXT_CHUNKS": 8,
        "MMR_FETCH_K_MULT": 5,
        "MMR_FETCH_K_MIN": 30,
        "MMR_LAMBDA_MULT": 0.60,
        "DEDUP_SIM_THRESHOLD": 0.94,
        "DEDUP_MAX_COMPARE": 160,
        "RETRIEVE_K_MULT": 2,
        "EVIDENCE_EXCERPT_CHARS": 1000,
    },
    "C": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1100,
        "CHUNK_OVERLAP": 160,
        "MAX_CHUNKS_PER_FILE": 1000,
        "TOP_K_PER_FILE": 4,
        "MAX_CONTEXT_CHUNKS": 12,
        "MMR_FETCH_K_MULT": 6,
        "MMR_FETCH_K_MIN": 40,
        "MMR_LAMBDA_MULT": 0.55,
        "DEDUP_SIM_THRESHOLD": 0.94,
        "DEDUP_MAX_COMPARE": 200,
        "RETRIEVE_K_MULT": 2,
    },
    "D": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 800,
        "CHUNK_OVERLAP": 200,
        "MAX_CHUNKS_PER_FILE": 2200,
        "TOP_K_PER_FILE": 7,
        "MAX_CONTEXT_CHUNKS": 22,
        "MMR_FETCH_K_MULT": 8,
        "MMR_FETCH_K_MIN": 60,
        "MMR_LAMBDA_MULT": 0.45,
        "DEDUP_SIM_THRESHOLD": 0.945,
        "DEDUP_MAX_COMPARE": 260,
        "RETRIEVE_K_MULT": 3,
        "EVIDENCE_EXCERPT_CHARS": 1400,
    },
    "E": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1200,
        "CHUNK_OVERLAP": 120,
        "MAX_CHUNKS_PER_FILE": 1200,
        "TOP_K_PER_FILE": 2,
        "MAX_CONTEXT_CHUNKS": 6,
        "MMR_FETCH_K_MULT": 5,
        "MMR_FETCH_K_MIN": 30,
        "MMR_LAMBDA_MULT": 0.72,
        "DEDUP_SIM_THRESHOLD": 0.95,
        "DEDUP_MAX_COMPARE": 200,
        "RETRIEVE_K_MULT": 1,
        "EVIDENCE_EXCERPT_CHARS": 1000,
    },
    "F": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1000,
        "CHUNK_OVERLAP": 140,
        "MAX_CHUNKS_PER_FILE": 1400,
        "TOP_K_PER_FILE": 5,
        "MAX_CONTEXT_CHUNKS": 14,
        "MMR_FETCH_K_MULT": 7,
        "MMR_FETCH_K_MIN": 50,
        "MMR_LAMBDA_MULT": 0.50,
        "DEDUP_SIM_THRESHOLD": 0.92,
        "DEDUP_MAX_COMPARE": 260,
        "RETRIEVE_K_MULT": 2,
    },
    "G": {
        "MAX_OUTPUT_TOKENS": 1536,
        "CHUNK_SIZE": 1100,
        "CHUNK_OVERLAP": 120,
        "MAX_CHUNKS_PER_FILE": 1400,
        "TOP_K_PER_FILE": 3,
        "MAX_CONTEXT_CHUNKS": 10,
        "MMR_FETCH_K_MULT": 6,
        "MMR_FETCH_K_MIN": 48,
        "MMR_LAMBDA_MULT": 0.70,
        "DEDUP_SIM_THRESHOLD": 0.92,
        "DEDUP_MAX_COMPARE": 260,
        "RETRIEVE_K_MULT": 2,
    },
    "H": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1000,
        "CHUNK_OVERLAP": 140,
        "MAX_CHUNKS_PER_FILE": 1600,
        "TOP_K_PER_FILE": 5,
        "MAX_CONTEXT_CHUNKS": 14,
        "MMR_FETCH_K_MULT": 10,
        "MMR_FETCH_K_MIN": 80,
        "MMR_LAMBDA_MULT": 0.52,
        "DEDUP_SIM_THRESHOLD": 0.92,
        "DEDUP_MAX_COMPARE": 260,
        "RETRIEVE_K_MULT": 2,
    },
    "I": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 950,
        "CHUNK_OVERLAP": 160,
        "MAX_CHUNKS_PER_FILE": 1600,
        "TOP_K_PER_FILE": 6,
        "MAX_CONTEXT_CHUNKS": 16,
        "MMR_FETCH_K_MULT": 8,
        "MMR_FETCH_K_MIN": 60,
        "MMR_LAMBDA_MULT": 0.40,
        "DEDUP_SIM_THRESHOLD": 0.92,
        "DEDUP_MAX_COMPARE": 260,
        "RETRIEVE_K_MULT": 2,
    },
    "J": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 750,
        "CHUNK_OVERLAP": 180,
        "MAX_CHUNKS_PER_FILE": 2200,
        "TOP_K_PER_FILE": 7,
        "MAX_CONTEXT_CHUNKS": 18,
        "MMR_FETCH_K_MULT": 8,
        "MMR_FETCH_K_MIN": 70,
        "MMR_LAMBDA_MULT": 0.48,
        "DEDUP_SIM_THRESHOLD": 0.92,
        "DEDUP_MAX_COMPARE": 260,
        "RETRIEVE_K_MULT": 2,
    },
    "K": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1400,
        "CHUNK_OVERLAP": 140,
        "MAX_CHUNKS_PER_FILE": 1200,
        "TOP_K_PER_FILE": 4,
        "MAX_CONTEXT_CHUNKS": 12,
        "MMR_FETCH_K_MULT": 7,
        "MMR_FETCH_K_MIN": 56,
        "MMR_LAMBDA_MULT": 0.58,
        "DEDUP_SIM_THRESHOLD": 0.92,
        "DEDUP_MAX_COMPARE": 260,
        "RETRIEVE_K_MULT": 2,
    },
    "L": {
        "MAX_OUTPUT_TOKENS": 1536,
        "CHUNK_SIZE": 1000,
        "CHUNK_OVERLAP": 120,
        "MAX_CHUNKS_PER_FILE": 1400,
        "TOP_K_PER_FILE": 4,
        "MAX_CONTEXT_CHUNKS": 12,
        "MMR_FETCH_K_MULT": 9,
        "MMR_FETCH_K_MIN": 72,
        "MMR_LAMBDA_MULT": 0.55,
        "DEDUP_SIM_THRESHOLD": 0.92,
        "DEDUP_MAX_COMPARE": 260,
        "RETRIEVE_K_MULT": 2,
    },
    "M": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1500,
        "CHUNK_OVERLAP": 150,
        "MAX_CHUNKS_PER_FILE": 1500,
        "TOP_K_PER_FILE": 6,
        "MAX_CONTEXT_CHUNKS": 18,
        "MMR_FETCH_K_MULT": 10,
        "MMR_FETCH_K_MIN": 80,
        "MMR_LAMBDA_MULT": 0.5,
    },

    "N": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1000,
        "CHUNK_OVERLAP": 140,
        "MAX_CHUNKS_PER_FILE": 1600,
        "TOP_K_PER_FILE": 7,
        "MAX_CONTEXT_CHUNKS": 20,
        "MMR_FETCH_K_MULT": 10,
        "MMR_FETCH_K_MIN": 80,
        "MMR_LAMBDA_MULT": 0.50,
    },

    "O": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1200,
        "CHUNK_OVERLAP": 160,
        "MAX_CHUNKS_PER_FILE": 1600,
        "TOP_K_PER_FILE": 6,
        "MAX_CONTEXT_CHUNKS": 16,
        "MMR_FETCH_K_MULT": 12,
        "MMR_FETCH_K_MIN": 100,
        "MMR_LAMBDA_MULT": 0.50,
    },

    "P": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1400,
        "CHUNK_OVERLAP": 180,
        "MAX_CHUNKS_PER_FILE": 1600,
        "TOP_K_PER_FILE": 6,
        "MAX_CONTEXT_CHUNKS": 18,
        "MMR_FETCH_K_MULT": 10,
        "MMR_FETCH_K_MIN": 80,
        "MMR_LAMBDA_MULT": 0.55,
    },

    "Q": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1000,
        "CHUNK_OVERLAP": 140,
        "MAX_CHUNKS_PER_FILE": 1800,
        "TOP_K_PER_FILE": 7,
        "MAX_CONTEXT_CHUNKS": 20,
        "MMR_FETCH_K_MULT": 12,
        "MMR_FETCH_K_MIN": 100,
        "MMR_LAMBDA_MULT": 0.48,
    },

    "R": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1200,
        "CHUNK_OVERLAP": 160,
        "MAX_CHUNKS_PER_FILE": 1800,
        "TOP_K_PER_FILE": 7,
        "MAX_CONTEXT_CHUNKS": 20,
        "MMR_FETCH_K_MULT": 12,
        "MMR_FETCH_K_MIN": 100,
        "MMR_LAMBDA_MULT": 0.50,
    },

    "S": {
        "MAX_OUTPUT_TOKENS": 2048,
        "CHUNK_SIZE": 1500,
        "CHUNK_OVERLAP": 180,
        "MAX_CHUNKS_PER_FILE": 1800,
        "TOP_K_PER_FILE": 8,
        "MAX_CONTEXT_CHUNKS": 24,
        "MMR_FETCH_K_MULT": 14,
        "MMR_FETCH_K_MIN": 120,
        "MMR_LAMBDA_MULT": 0.45,
    }
}

if choice not in CONFIGS:
    raise ValueError(f"Unknown choice: {choice}")

cfg = CONFIGS[choice]

MAX_OUTPUT_TOKENS = cfg["MAX_OUTPUT_TOKENS"]
CHUNK_SIZE = cfg["CHUNK_SIZE"]
CHUNK_OVERLAP = cfg["CHUNK_OVERLAP"]
MAX_CHUNKS_PER_FILE = cfg["MAX_CHUNKS_PER_FILE"]
TOP_K_PER_FILE = cfg["TOP_K_PER_FILE"]
MAX_CONTEXT_CHUNKS = cfg["MAX_CONTEXT_CHUNKS"]

MMR_FETCH_K_MULT = cfg.get("MMR_FETCH_K_MULT")
MMR_FETCH_K_MIN = cfg.get("MMR_FETCH_K_MIN")
MMR_LAMBDA_MULT = cfg.get("MMR_LAMBDA_MULT")
'''
DEDUP_SIM_THRESHOLD = cfg.get("DEDUP_SIM_THRESHOLD", DEDUP_SIM_THRESHOLD)
DEDUP_MAX_COMPARE = cfg.get("DEDUP_MAX_COMPARE", DEDUP_MAX_COMPARE)
RETRIEVE_K_MULT = cfg.get("RETRIEVE_K_MULT", RETRIEVE_K_MULT)

STREAM_DELAY = cfg.get("STREAM_DELAY", STREAM_DELAY)
EVIDENCE_EXCERPT_CHARS = cfg.get("EVIDENCE_EXCERPT_CHARS", EVIDENCE_EXCERPT_CHARS)'''