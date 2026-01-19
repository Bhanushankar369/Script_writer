from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from typing import Annoatated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annoatated[list, add_messages]