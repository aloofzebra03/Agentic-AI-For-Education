# pdf_loader.py

from langchain_community.document_loaders import PyPDFLoader
from Creating_Section_Text import config

def load_documents():
    loader = PyPDFLoader(config.PDF_PATH)
    # each page → one Document
    return loader.load()
