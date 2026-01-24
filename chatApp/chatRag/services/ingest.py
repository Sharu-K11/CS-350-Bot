import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[3]   # CHATBOT/
PDF_PATH = BASE_DIR / "chatApp" / "chatRag" / "data" / "material.pdf"


def ingest_documents():
    # Path for the book pdf
    loader = PyPDFLoader(str(PDF_PATH))
    return loader.load()


if __name__ == "__main__":
    pass
