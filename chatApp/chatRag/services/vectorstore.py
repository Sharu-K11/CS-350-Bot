from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import Chroma

from .ingest import ingest_documents   

import os
from pathlib import Path

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

PARENT_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = PARENT_DIR / "chroma_db"


def make_chunks():
    documents = ingest_documents()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 1000,
        chunk_overlap = 100 ,
        length_function = len ,
        separators=["\n\n","\n","."," ","   ",""]

    )


    chunks = text_splitter.split_documents(documents)

    return chunks


def build_vectorstore():
    chunks = make_chunks()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=str(CHROMA_DIR),
        collection_name='cs350_docs'
    )

    return vectorstore

# load existing DB (this is what the chain should use)
def get_vectorstore():
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=OpenAIEmbeddings(),
        collection_name="cs350_docs",
    )


if __name__ == "__main__":
    # chunks = make_chunks()
    # print(f'lenth of the chunks {len(chunks)}')
    # print(f"\nChunk example:")
    # print(f"Content: {chunks[0].page_content[:150]}...")
    # print(f"Metadata: {chunks[0].metadata}")

    vs = build_vectorstore()
    result = vs.similarity_search(query="What is binary",k=3)
    print(result)


