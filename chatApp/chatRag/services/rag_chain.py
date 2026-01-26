from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

from .vectorstore import get_vectorstore


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_pipeline():
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_template("""
    You are a CS:APP teaching assistant. Use ONLY the provided CONTEXT (the book/notes).
    Do not use outside knowledge.

    If the answer is not in the context, reply exactly:
    "I don't know based on the provided documents."

    Output format (always):
    1) Quick Answer (1–2 sentences)
    2) Explanation (3–6 sentences, simple → slightly deeper)
    3) Key Evidence (1–2 short paraphrases of what in the context supports the answer)
    4) Practice Problem (based ONLY on context; no solution unless student explicitly asks)

    CONTEXT:
    {context}

    QUESTION:
    {question}

    RESPONSE:
    """)


    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# --- quick test runner ---
if __name__ == "__main__":
    # Build once
    chain = build_pipeline()

    # Quick fixed tests
    test_questions = [
        "What is a TLB?",
        "Explain cache associativity in simple terms.",
        "What is the difference between a page fault and a TLB miss?",
    ]

    print("\n=== RAG Chain Smoke Test ===\n")
    for i, q in enumerate(test_questions, 1):
        print(f"\n[{i}] QUESTION: {q}")
        try:
            ans = chain.invoke(q)
            print(f"ANSWER:\n{ans}")
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")

