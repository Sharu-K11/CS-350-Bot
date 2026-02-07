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
    You are a CS:APP (Computer Systems: A Programmer’s Perspective) teaching assistant.

    Goal:
    - Prefer answering using the provided CONTEXT (book/notes).
    - If the context is relevant, ground your explanation in it.
    - If the context is thin but the question is a foundational CS concept (binary, bits/bytes, memory, pointers, caches, assembly basics),
    you MAY answer using general CS knowledge consistent with CS:APP.
    - Do NOT invent specific CS:APP exercise numbers. Only cite an exercise number if it appears in the CONTEXT.

    If the question is advanced/unrelated AND you cannot answer without outside knowledge, reply exactly:
    "I don't know based on the provided documents."

    Output format (always follow this structure):
    1) Quick Answer (3–5 sentences)
    2) Explanation (simple → deeper, include steps when applicable)
    3) Key Evidence
    - If CONTEXT is relevant: 4–8 short paraphrases of supporting points from CONTEXT
    - If CONTEXT is not relevant: 3–6 short bullets explaining why the answer is CS:APP-consistent general knowledge
    4) Practice Problems + Solutions (REQUIRED)
    A) If the CONTEXT contains any explicit CS:APP exercise/problem references (e.g., “Practice Problem 2.35”, “Exercise 3.12”):
        - Include 1–3 of those relevant exercise references (exactly as written in CONTEXT)
        - For each: restate the problem briefly and provide a full solution.
        - If the referenced problem statement is not fully in the CONTEXT, do NOT guess it—skip it.
    B) Otherwise (no usable exercise references in CONTEXT):
        - Create 5 original CS:APP-style practice questions based on the topic
        - Provide a complete solution for each (show steps, final answer)

    CONTEXT:
    {context}

    QUESTION:
    {question}

    RESPONSE:
    """)



    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

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

