import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from typing import TypedDict, Optional, Annotated
from langgraph.graph.message import add_messages


load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
search_tool = TavilySearchResults(max_results=2)


class AIAgent(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def router_node(state: AIAgent):
    # Extract latest user message only
    user_query = state["messages"][-1].content

    prompt = f"""
    Decide whether the following question requires
    live or recent internet information.

    Respond with EXACTLY one word:
    - search
    - respond

    Question: {user_query}
    """

    result = llm.invoke([HumanMessage(content=prompt)])
    result_response = result.content.strip().lower()
    if "search" in result_response:
        return "search"
    return "respond"


def search_node(state: AIAgent):
    user_query = state["messages"][-1].content
    result = search_tool.run(user_query)
    return {"messages": [HumanMessage(content=f"Search Results:\n{result}")]}


def respond(state: AIAgent):
    result = llm.invoke(state["messages"])
    return {"messages": [result]}


def build_graph():
    graph = StateGraph(AIAgent)
    graph.add_node("search_node", search_node)
    graph.add_node("respond", respond)

    # Adding Conditional Edge
    graph.set_conditional_entry_point(
        router_node, {"search": "search_node", "respond": "respond"}
    )

    graph.add_edge("search_node", "respond")

    graph.add_edge("respond", END)

    return graph.compile()


graph = build_graph()
