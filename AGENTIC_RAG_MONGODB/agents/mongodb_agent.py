import yaml
import ast
from pathlib import Path
from AGENTIC_RAG_MONGODB.state.AgentState import AgentState
from AGENTIC_RAG_MONGODB.tools.clean_text import clean_text
from AGENTIC_RAG_MONGODB.tools.mongodb import get_results_mongo
from AGENTIC_RAG_MONGODB.api.api_key import get_api_key
from AGENTIC_RAG_MONGODB.embeddings.transformers import reranker

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage,AIMessage
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate

#python -m AGENTIC_RAG_MODULAR.workflows.planner_agent

config_path = Path("AGENTIC_RAG_MONGODB/config/configuration.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)


class mongotool:
    def __init__(self, api_key: str):
        if config:
            self.api_key = api_key
            self.model=config['groq']['llm3']['model_name']
            self.llm=ChatGroq(model_name=self.model,api_key=self.api_key)
            # print(self.model , self.llm)

        else:
            return 'No LLM initialized'
 
     #CREATE AGENTS TO WRAP THE TOOLS

    def mongo_db_tool(self,state: AgentState):
        print("--- VERIFYING THE EMBEDDINGS FOR MONGO DB ---")
        query= state['topic']
        msg_resp=state['messages'][-1].content[-1]
        chunks=state['chunks']
        org_query=state['messages'][-1].content[0]
        
        
        
        rs_lst=msg_resp.split('\n')
        fin=[y.replace('"','') for y in rs_lst]
        fin_lst=[x.split(':') for x in fin ]

        vals=[]
        for x in range(len(fin_lst)):
            if fin_lst[x][2].strip(" ").strip("'") == 'get_results_mongo':
                vals.append(fin_lst[x][1].strip(" ").strip("'"))
        qts=''.join(vals)
        
    
        try:
            agent = create_agent(
            tools=[get_results_mongo] ,
            model=self.llm,
            system_prompt="""You are a smart tool assistant. Using the tool specified answer the content . 
            If the context does not match with any tool description return : NO DATA AVAILABLE """
            )

            response = agent.invoke({'messages':[{'role':'user',"content":f'{qts}'}]})
            
            tool_messages = [
                m for m in response["messages"]
                if isinstance(m, ToolMessage)
            ]
            if len(tool_messages) == 0:
                ai_messages = [
                m for m in response["messages"]
                if isinstance(m, AIMessage)
                ]
                print('No Tools available')
                
                return {
                        'messages':[org_query]+[ai_messages],
                        'topic':query,
                        'chunks': chunks,
                        'task_state' : 'NO DATA FETCHED'
                        }
            else:
                print('TOOLS AVAILABLE')
                results = ast.literal_eval(tool_messages[0].content)
                pair=[]
                for tx in range(len(results)):
                    pair.append((query,results[tx][1]))
                rerank_scores = reranker.predict(pair)
                positive_pairs = [
                        vl for vl, score in zip(pair, rerank_scores) if score > 0
                    ]
                # print(positive_pairs)
                if len(positive_pairs)==0:
                    return {
                        'messages':[org_query]+['No details found'],
                        'topic':query,
                        'chunks': chunks,
                        'task_state' : 'NO DATA FETCHED'
                        }
                    # return {'messages': [messages]+['No details found']}
                else:
                    details=[clean_text(text) for _, text in positive_pairs]
                    details=','.join(details)

                    
                    chunks['mongo_db'].append(details)
                    return {
                        'messages':[HumanMessage(content=[org_query]+[msg_resp])],
                        'topic':query,
                        'chunks': chunks,
                        'task_state' : 'DATA FETCHED'
                        }
                    
                    
                    

        except Exception as e:
            err= f"TOOL ERROR: {repr(e)}"   
            return {
                        'messages':[HumanMessage(content=[org_query]+[err])],
                        'topic':query,
                        'chunks': ['No details found'],
                        'task_state' : 'NO DATA FETCHED'
                        }
    

    

                

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
#         logger = mongotool(api_key).mongo_db_tool(val)
#         print(logger)
#     except Exception as e:
#         print(e)
        
        