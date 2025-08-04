from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from typing import TypedDict, Literal, Annotated
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
llm = ChatGroq(model="Gemma2-9b-It",temperature=0)

def chat_node(state: ChatState):
    # take the user query from state
    messages = state['messages']
    
    # send to llm
    response = llm.invoke(messages)
    
    # response store state
    return {
        'messages': [response]
    }
    
checkpointer = MemorySaver()
graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
workflow = graph.compile(checkpointer=checkpointer)