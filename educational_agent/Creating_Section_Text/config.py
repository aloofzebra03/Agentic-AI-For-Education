
import os
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

MODEL_NAME     = "gemini-2.0-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

HF_API_KEY          = os.getenv("HF_API_KEY", "")
# HF_EMBEDDING_MODEL  = "sentence-transformers/all-mpnet-base-v2"
HF_EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# Chroma
CHROMA_PERSIST_DIR = "chroma_db"

# PDF to ingest
PDF_PATH = r"data/Chapter8.pdf"

TEST_PARAMS_PATH = "test/params.json"
