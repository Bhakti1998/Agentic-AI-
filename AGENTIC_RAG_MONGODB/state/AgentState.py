from typing import Sequence,TypedDict, Annotated , Dict , List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage,ToolMessage
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]
    topic:str=None
    chunks: Dict[str, List[str]]
    task_state : str=''