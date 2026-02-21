import yaml
from pathlib import Path
from AGENTIC_RAG_MONGODB.state.AgentState import AgentState
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from AGENTIC_RAG_MONGODB.api.api_key import get_api_key
#python -m AGENTIC_RAG_MODULAR.workflows.planner_agent

config_path = Path("AGENTIC_RAG_MONGODB/config/configuration.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)


class Verifier:
    def __init__(self, api_key: str):
        if config:
            self.api_key = api_key
            self.model=config['groq']['llm1']['model_name']
            self.llm=ChatGroq(model_name=self.model,api_key=self.api_key)
            # print(self.model , self.llm)

        else:
            return 'No LLM initialized'
 
    #CREATE VERIFIER AGENT TO VERIFY THE CHUNKS FROM TOOLS
    def verifier_agent(self,state: AgentState):
        print("--- VERIFYING THE DATA ---")
        """VERIFIER AGENT TO CHECK IF RELEVANT INFORMATION IS AVAILABLE"""
        
        question = state['messages'][-1].content[0]  #"'Step1': 'How to create a Mongo Db Database': 'get_results_mongo'\n'Step2': 'explain self attention mechanism': 'get_query_results_attn'\n'Step3': 'explain roman numeals': 'NONE'"#state['messages'][0].content
        chunks= state['chunks']
        info_mongo=''
        info_attn=''
        for val in chunks:
            if len(chunks['mongo_db']) != 0:
                info_mongo=' '.join(chunks['mongo_db'])
            if len(chunks['mongo_db']) != 0:
                info_attn=' '.join(chunks['attn_paper'])

        

    
        system_msg = SystemMessage (content= f"""
        You are an intelligent comparison agent that compares user query and chunks extracted from the tools semantically and checks if the chunks are valid enough to answer a query.
        Follow the below instructions:
            1.Take user query : {question} and the chunks for Topic Mongo DB {info_mongo} and Topic 'ATTENTION IS ALL YOU NEED' paper {info_attn}
            2.Understand the info details and verify if the chunks in both are good enough to answer a user query
            3.If the chunks are incomplete or not enough to answer the query , reply strictly with the following along with the question that requires more context:
            1.'MAKE_ANOTHER_TOOL_CALL' : <question>
            Example: Question: 'What is Mongo db and what is encoder'
            Reply: 'MAKE_ANOTHER_TOOL_CALL' : what is encoder
            4.If the chunks are complete and good enough to answer the query reply strictly with the following:
            2.'GENERATE_ANSWER'
            5.Reply with either 'MAKE_ANOTHER_TOOL_CALL' : <question> or 'GENERATE_ANSWER' . Not both replies together

            Strictly follow the instructions:
            1.Do not add extra text in your reply 
            2.Do not add thinking steps 
            3.Do not hallucinate anything apart from details provided to you explicitly


            Please answer the following query
            Question:
            {question}
            by leveraging  the context provided below
            Context:
            Topic Mongo DB  : {info_mongo}
            Topic 'ATTENTION IS ALL YOU NEED' paper : {info_attn} """)

        try:
            result = self.llm.invoke([system_msg]+[question])
            
            if 'MAKE_ANOTHER_TOOL_CALL' in result.content:
                res=result.content
                query=res.split(':')[1].strip(' ')
                
                task_state='MAKE_ANOTHER_TOOL_CALL'
            else:
                query=question
                
                task_state='VERIFICATION DONE'

            
            return {
                        'messages':[HumanMessage(content=[question]+[result.content])],
                        'topic':query,
                        'chunks': chunks,
                        'task_state' : task_state
                        }
            

        except Exception as e:
                err= f"ERROR: {repr(e)}"   
                print('VERIFICATION PROCESS FAILED')
                return {
                        'messages':[HumanMessage(content=[question]+[err])],
                        'topic':query,
                        'chunks': chunks,
                        'task_state' : 'VERIFICATION FAILED'
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
#         logger = Verifier(api_key).verifier_agent(val)
#         print(logger)
#     except Exception as e:
#         print(e)
        
        