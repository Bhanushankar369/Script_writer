from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from typing import Annoatated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annoatated[list, add_messages]
    
    
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)

def chatBot(state: State):
    return {"messages": [llm.invoke(state['messages'])]}


graph = StateGraph(State)

# Node creation
graph.add_node("chatBot", chatBot)

# Edges
graph.add_edge(START, "chatBot")
graph.add_edge("chatBot", END)

graph_build = graph.compile()
