# AI Agent Backend with LangGraph + FastAPI + Docker

A production-ready AI agent backend built using **LangGraph**, **FastAPI**, and **Docker**.  
This project demonstrates AI orchestration, optional search integration, API safety, and containerized deployment.

---

## 🚀 Features

- 🔀 LangGraph-based workflow with conditional routing
- 🔍 Optional web search using Tavily
- ⚡ Async FastAPI backend
- 🛑 Timeout protection for LLM calls
- 📝 File-based logging
- 🔐 Environment-based API key management
- 🐳 Dockerized for portable deployment

---

## 🧠 Architecture

Client  
↓  
FastAPI Backend  
↓  
LangGraph Workflow  
↓  
Router Node  
→ (If needed) Search Node (Tavily)  
→ LLM Response (Gemini)  
↓  
Return Response  

---

## 📦 Tech Stack

- Python 3.11
- FastAPI
- LangGraph
- LangChain
- Google Gemini API
- Tavily Search
- Docker

---

## ⚙️ Environment Variables

Create a `.env` file:


GOOGLE_API_KEY=your_google_api_key

TAVILY_API_KEY=your_tavily_api_key


⚠️ Never commit `.env` to GitHub.

---

## 🖥️ Run Locally (Without Docker)

```bash
pip install -r requirements.txt
uvicorn backend:app --reload

Open:

http://localhost:8000/docs
🐳 Run with Docker

Build image:

docker build -t chatbot .

Run container:

docker run -p 8000:8000 --env-file .env chatbot

Open:

http://localhost:8000/docs
📡 API Endpoint
POST /chat

Request Body:

{
  "message": "Hello"
}

Response:

{
  "response": "Hi there! How can I help you?"
}