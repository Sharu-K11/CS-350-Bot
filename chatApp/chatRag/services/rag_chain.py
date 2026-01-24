from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

from .vectorstore import get_vectorstore


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_pipeline():
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_template(
        """
        You are a teaching assistant. Use the context to help the student understand.

        Rules:
        - Use ONLY the provided context for factual information.
        - Explain in simple terms first, then add more detail.
        - If the question is about a concept, structure the answer as:
        1) Short definition
        2) Intuition
        3) Tiny example
        4) Common mistake to avoid
        - If the topic involves logic, reasoning, math, algorithms, or problem-solving AND the student asks for practice:
        - Include one short practice problem based ONLY on the context
        - Do NOT include the solution unless the student explicitly asks
        - If the answer is not in the context, say:
        "I don't know based on the provided documents."

        CONTEXT:
        {context}

        STUDENT QUESTION:
        {question}

        TEACHING ANSWER:
        """
    )

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

