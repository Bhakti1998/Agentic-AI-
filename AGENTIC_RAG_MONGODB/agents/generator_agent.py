import yaml
from pathlib import Path
from AGENTIC_RAG_MONGODB.state.AgentState import AgentState
from AGENTIC_RAG_MONGODB.api.api_key import get_api_key
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate

#python -m AGENTIC_RAG_MODULAR.workflows.planner_agent

config_path = Path("AGENTIC_RAG_MONGODB/config/configuration.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)



class Generator:
    def __init__(self, api_key: str):
        if config:
            self.api_key = api_key
            self.model=config['groq']['llm2']['model_name']
            self.llm=ChatGroq(model_name=self.model,api_key=self.api_key)
            

        else:
            return 'No LLM initialized For generator agent'
 

    #CREATE GENERATOR AGENT FOR ANSWERING
    def generator_agent(self,state: AgentState):
        print("--- GENERATING THE ANSWER ---")
        """GENERATOR AGENT TO PROVIDE RELEVANT ANSWER BY USING THE CHUNKS"""
        
        question = state['messages'][-1].content[0]
        chunks_mongo= ','.join(state['chunks']['mongo_db'])
        chunks_attn= ','.join(state['chunks']['attn_paper'])
        chunks = state['chunks']
        
        
        system_msg = SystemMessage (content= f"""
        You are an intelligent agent with good experience in understnding content and providing answers
        You can answer a user's questions in all aspects of the query asked by the user on topics of Mongo Db and the paper Attention is all you need.
        Please answer the following query
        Question:
        {question}
        by leveraging the context details provided below
        Context:
        {chunks_mongo} 
        {chunks_attn}
        
        
        Instructions to be followed:
        -- Understand the chunks {chunks_mongo} and {chunks_attn}. Provide the answer to best of your understanding of the chunks and your own knowledge.
        -- If the context does not contain information to answer the question, reply: "No data available.""
        -- Generate the answer in a detailed and concise manner covering all the aspects of the query
        -- Generate answer only relevant to the query asked
        -- Do not add any irrelevant data in the answer 
        -- Anwer should be detailed and in only 10-20 lines strictly. 

        Answer in following format :
        1.Question:{question}
        Generated Answer:
        --> Answer here                                                                                 
        """)

        result = self.llm.invoke([system_msg]+[question])
        
        return {'messages':[HumanMessage(content=[question]+[result.content])],
                        'topic':question,
                        'chunks': chunks,
                        'task_state' : 'GENERATION COMPLETE'
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
#         logger = Generator(api_key).generator_agent(val)
#         print(logger)
#     except Exception as e:
#         print(e)
        
        