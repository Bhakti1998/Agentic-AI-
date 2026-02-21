from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from AGENTIC_RAG_MONGODB.state.AgentState import AgentState
from AGENTIC_RAG_MONGODB.agents import planner_agent , verifier_agent , generator_agent
from AGENTIC_RAG_MONGODB.agents import mongodb_agent , attention_paper_agent
from AGENTIC_RAG_MONGODB.router.tools_condition import tools_condition 
from AGENTIC_RAG_MONGODB.router.verifier_condition import verifier_condition


class WorkflowAgent:
    def __init__(self,api_key: str):
        self.api_key = api_key
        self.mongo_db_tool = mongodb_agent.mongotool(self.api_key).mongo_db_tool
        self.attention_paper_tool = attention_paper_agent.attentiontool(self.api_key).atten_tool
        self.planner_agent = planner_agent.Planner(self.api_key).planner_agent
        self.verifier_agent = verifier_agent.Verifier(self.api_key).verifier_agent
        self.generator_agent = generator_agent.Generator(self.api_key).generator_agent
        


    def langchain_workflow(self):
        print('GRAPH COMPILATION IN PROGRESS')
        workflow=StateGraph(AgentState)
        workflow.add_node("PLANNER", self.planner_agent) 
        workflow.add_node("MONGO_DB_TOOL", self.mongo_db_tool)
        workflow.add_node("ATTN_TOOL", self.attention_paper_tool)
        workflow.add_node("VERIFY", self.verifier_agent)
        workflow.add_node("O/P generator", self.generator_agent)
        workflow.set_entry_point("PLANNER")

        workflow.add_conditional_edges("PLANNER",
                                    tools_condition,
                                    {"MONGODB_TOOL": "MONGO_DB_TOOL",
                                    "ATTENTION_TOOL" : "ATTN_TOOL",
                                        "DONE" : END,
                                        })


        workflow.add_edge("MONGO_DB_TOOL", "VERIFY")
        workflow.add_edge("ATTN_TOOL", "VERIFY")
        workflow.add_conditional_edges("VERIFY",
                                    verifier_condition,
                                    {"GENERATE": "O/P generator",
                                    "REPLAN" : "PLANNER",
                                    "DONE":END
                                    
                                        })

                           
        workflow.add_edge("O/P generator", END)
        final_workflow=workflow.compile()
        return final_workflow
