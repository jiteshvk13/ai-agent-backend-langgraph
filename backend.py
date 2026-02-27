from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, BaseMessage
from ai_agent import graph
import asyncio
from logging_config import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

app = FastAPI(title="Ai Agent Backend", description="Langgraph Ai Agent With Search")


# Pydantic Model
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
async def health_check():
    return {"status": "Backend Running"}


# Chat Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"Incoming message: {request.message}")
        initial_state = {"messages": [HumanMessage(content=request.message)]}

        result = await asyncio.wait_for(graph.ainvoke(initial_state), timeout=20)
        final_answer = result["messages"][-1].content

        logger.info("Response generated successfully")
        return ChatResponse(response=final_answer)

    except asyncio.TimeoutError:
        logger.error("LLM request timed out")
        raise HTTPException(status_code=504, detail="Request timed out")

    except Exception:
        logger.exception("Error during chat processing")
        raise HTTPException(status_code=500, detail="Internal server error")
