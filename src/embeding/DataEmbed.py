"""
DataGenerator  –  folder-driven embedder
------------------------------------------------
Usage:
    python DataEmbed.py /Users/siddhartha.singh/scaningBee/resources
"""

from __future__ import annotations
from pathlib import Path
import os, sys, re, unicodedata, argparse, tqdm
# from langchain.embeddings import OllamaEmbeddings
# from langchain.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings   # change if you prefer HF
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ------------------ configuration knobs ------------------

FILE_EXTS       = {".ps1", ".groovy", ".txt", ".md"}   # edit as needed
CHUNK_SIZE      = 1024
CHUNK_OVERLAP   = 200
CHROMA_DIR      = "db"          # will be created if missing
EMBED_MODEL     = "nomic-embed-text"

# ---------------------------------------------------------

embeddings = OllamaEmbeddings(model=EMBED_MODEL, show_progress=True)
splitter   = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,
                                            chunk_overlap=CHUNK_OVERLAP)

vectorstore = Chroma(embedding_function=embeddings,
                     persist_directory=CHROMA_DIR)

def slug(text: str) -> str:
    txt = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    txt = re.sub(r"[^A-Za-z0-9]+", "_", txt).strip("_").lower()
    return txt or "root"

def label_for(path: Path, root: Path) -> str:
    """Turn folder hierarchy into `foo_bar_baz`."""
    rel = path.parent.relative_to(root)
    return slug("_".join(rel.parts)) if rel.parts else "root"

def ingest_file(path: Path, root: Path):
    label = label_for(path, root)
    with path.open("r", encoding="utf-8", errors="ignore") as fh:
        text = fh.read()

    # break large files into chunks so query-time recall is better
    chunks = splitter.split_text(text)
    metas  = [{"label": label, "path": str(path)}] * len(chunks)

    vectorstore.add_texts(chunks, metadatas=metas)

def crawl_and_ingest(root_dir: Path):
    files = [p for p in root_dir.rglob("*") if p.suffix.lower() in FILE_EXTS]
    print(f"🗂  Found {len(files)} files under {root_dir}")
    for f in tqdm.tqdm(files, desc="Embedding"):
        ingest_file(f, root_dir)
    vectorstore.persist()
    print(f"✅  Finished. Vectors stored in {CHROMA_DIR}/")

# -------------------- command-line run -------------------

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Generate embeddings from a folder tree")
    ap.add_argument("folder", type=Path, help="Top-level folder containing labelled sub-folders")
    args = ap.parse_args()

    if not args.folder.is_dir():
        sys.exit(f"ERR: {args.folder} is not a directory")

    crawl_and_ingest(args.folder.resolve())
