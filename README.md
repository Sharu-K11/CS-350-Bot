# 📚 CS-350 RAG Chatbot

A **Django-based Retrieval-Augmented Generation (RAG) chatbot** built to assist with **CS-350 (Computer Systems)** concepts such as caches, virtual memory, paging, pipelines, and related topics.  
The chatbot retrieves relevant course material using a vector database and generates **context-grounded, teaching-style responses**.

---

## ✨ Features

- 🔍 **Retrieval-Augmented Generation (RAG)**
- 🧠 **Teaching-style responses** (definition, intuition, example, common mistakes)
- 📄 PDF / notes ingestion using embeddings
- 📦 **ChromaDB** for vector storage
- ⚙️ **LangChain (LCEL)** for clean, declarative pipelines
- 🌐 Django backend
- 📓 Jupyter notebooks for experimentation & ingestion
- 🔐 Secrets handled safely via environment variables

---

## 🏗️ Tech Stack

- **Backend:** Django
- **LLM Framework:** LangChain (LCEL)
- **Vector Store:** ChromaDB (local)
- **Embeddings:** OpenAI embeddings
- **Language:** Python
- **Notebooks:** Jupyter
- **Version Control:** Git + GitHub

---

## 📂 Project Structure

```text
CHATBOT/
│
├── chatApp/               # Django app (views, logic, RAG integration)
├── chatbot/               # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS)
│
├── notebook/
│   ├── test_notebook.ipynb # Experimentation / ingestion notebook
│   └── chroma_db/          # Local vector DB (ignored by git)
│
├── manage.py
├── requirements.txt
├── .gitignore
└── .env                    # Local secrets (NOT committed)
