import json
import hashlib
from pathlib import Path

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def cache_path_for(cache_root: Path, file_hash: str) -> Path:
    return cache_root / file_hash

def has_cached_index(path: Path) -> bool:
    return (path / "index.faiss").exists() and (path / "index.pkl").exists()

def save_manifest(path: Path, manifest: dict):
    path.mkdir(parents=True, exist_ok=True)
    with open(path / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

def clear_cache_dir(cache_root: Path):
    for p in cache_root.glob("*"):
        if p.is_dir():
            for child in p.glob("*"):
                child.unlink(missing_ok=True)
            p.rmdir()