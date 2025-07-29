# vectorstore.py

import os
from pathlib import Path

from langchain_chroma import Chroma
from Creating_Section_Text.embedder       import get_embedder
from Creating_Section_Text.pdf_loader     import load_documents
from Creating_Section_Text import config

DB_DIR  = Path(config.CHROMA_PERSIST_DIR)
DB_FILE = DB_DIR / "chroma.sqlite3"   # the primary SQLite file Chroma uses

def build_vectorstore():

    if DB_FILE.exists():
        print(f" Vector store already exists at {DB_FILE!r}; skipping rebuild.")
        # You could still load it here if you wanted to return a Chroma object:
        return None

    # Otherwise, ingest and persist:
    docs     = load_documents()
    print(f"{len(docs)} documents loaded.")
    embedder = get_embedder()
    print("Building vector store…")

    vector_store = Chroma.from_documents(
        documents        = docs,
        embedding         = embedder,
        persist_directory = str(DB_DIR),
        collection_name   = "chapter8"
    )
    print(f"Vector store built at {DB_FILE!r}.")
    return vector_store


def load_vectorstore():
    if not DB_FILE.exists():
        print(f"No vector store found at {DB_FILE!r}.")
        print("Please run: python main.py ingest")
        raise FileNotFoundError(f"Vector store not found at {DB_FILE!r}")

    embedder = get_embedder()
    vs = Chroma(
        persist_directory   = str(DB_DIR),
        embedding_function  = embedder,
        collection_name     = "chapter8"
    )
    print(f"Vector store loaded. Indexed documents: {vs._collection.count()}")
    return vs
