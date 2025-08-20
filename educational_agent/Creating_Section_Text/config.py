
import os
from dotenv import load_dotenv

import streamlit as st

# GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

load_dotenv()

MODEL_NAME     = "gemini-2.0-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

HF_API_KEY          = os.getenv("HF_API_KEY", "")
# HF_EMBEDDING_MODEL  = "sentence-transformers/all-mpnet-base-v2"
HF_EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# Chroma
CHROMA_PERSIST_DIR = "educational_agent/Creating_Section_Text/chroma_db"

# PDF to ingest
PDF_PATH = r"Creating_Section_Text/data/Chapter8.pdf"

TEST_PARAMS_PATH = "Creating_Section_Text/test/params.json"
