import yaml
from pathlib import Path
from AGENTIC_RAG_MONGODB.state.AgentState import AgentState
from AGENTIC_RAG_MONGODB.state.TOOL_SCOPE import TOOL_SCOPE
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate
from AGENTIC_RAG_MONGODB.api.api_key import get_api_key
#python -m AGENTIC_RAG_MODULAR.workflows.planner_agent

config_path = Path("AGENTIC_RAG_MONGODB/config/configuration.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)


class Planner:
    def __init__(self, api_key: str):
        
        if config:
            self.api_key = api_key
            self.model=config['groq']['llm1']['model_name']
            self.llm=ChatGroq(model_name=self.model,api_key=self.api_key)
            # print(self.model , self.llm)

        else:
            return 'No LLM initialized'
 
    def planner_agent(self,state: AgentState):  
        print("--- PLAN THE STEPS FOR THE EXECUTION ---")
        query= state['topic'] 
        chunks=state['chunks']
        task_state=state['task_state']

        if task_state=='MAKE_ANOTHER_TOOL_CALL':
            org_query=state['messages'][-1].content[0]
        else:
            org_query=query
        details = TOOL_SCOPE

        prompt=PromptTemplate(
                template= f""" 
                            1.You are an intelligent planner agent who is good at planning steps by breaking down a user question and understanding the details provided.
                            2.Understand user query and if the query has multiple domains , separate the query into multiple sub-questions else don't
                            3.Understand a user question {query} and {details} identify which sub questions can be answered by which tool. 
                            4.In the available tools {details} match one-to-one which tool can answer a sub-question
                            5.Once decided , Plan steps on which sub-question to be answered first and using which tool name
                            6.If the question or sub-question does not relate to any tool provided reply with 'NONE'
                            7.Once decided , strictly reply in the following formats only: 
                            For Example:
                            Question1: What is Mongo Db and what is attention mechanism?
                            

                            Reply only in this format : 'Step1': 'What is Mongo Db':'get_results_mongo'
                                                        'Step2': 'what is attention mechanism':'get_query_results_attn'
                            Question2: What is atomic theory and collections in MongoDB?
                            
                            Reply only in this format : 'Step1': 'What is atomic theory': 'NONE'
                                                        'Step2': 'collections in MongoDB': 'get_results_mongo'
    
                            8. Only reply with the steps as shown above , no extra text or explanation or your thinking steps to be added in the reply
                            

                            NOT TO DO (Strictly):
                            - DO NOT use external knowledge , only use details here:{details}
                            - DO NOT hallucinate any extra data in replies , Tool Scopes or invent tools
                            - DO NOT change the Tool names , the names should be an exact match.
                            - Strictly only plan further steps , do not provide any answer yourself
                            - Strictly No Thinking steps and no question to be added in the final reply

                            Here is user query: {query}
                            Here is the tool scope : {details}  
                                            
                            """,
                            input_variables=["query","details"]
            
            )
        chain= prompt | self.llm
        try:
            response=chain.invoke({"query": org_query, "details": TOOL_SCOPE})
            
            print(response.content)
            if 'MAKE_ANOTHER_TOOL_CALL' in task_state:
                print('---REPLANING DONE----')
                task_state = 'REPLANING DONE'
            else:
                print('---PLANING DONE----')
                task_state = 'PLANNING DONE'


            
            return {
            'messages': [HumanMessage(content=[org_query]+[response.content])],
            'topic': query,
            'chunks': chunks,
            'task_state' : task_state
            
        }
        except Exception as e:
                err= f"ERROR: {repr(e)}"   
                print('---PLANING FAILED . STOPPING PROCESS----')
                return {
                    'messages':[HumanMessage(content=[org_query]+[err])],
                    'topic':query,
                    'chunks': chunks,
                    'task_state' : 'PLANNING FAILED'}
                

# if __name__ == "__main__":
#     try:
#         api_key=get_api_key('GROQ_API_KEY')
#         val={'messages': [HumanMessage(content="How to create a Mongo Db Database")],
#             'topic':'How to create a Mongo Db Database',
#             'chunks':{
#                 'mongo_db': [],
#                 'attn_paper': []
#                 },
#             'task_state' : 'START'}
#         logger = Planner(api_key).planner_agent(val)
#         print(logger)
#     except Exception as e:
#         print(e)
        
        