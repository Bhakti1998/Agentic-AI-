from AGENTIC_RAG_MONGODB.workflow import langgraph_workflow
from pathlib import Path
from langchain_groq import ChatGroq
from AGENTIC_RAG_MONGODB.api.api_key import get_api_key
from AGENTIC_RAG_MONGODB.state import AgentState
from langchain_core.messages import HumanMessage

class AgenticFlow:
    def __init__(self, api_key: str):
        self.api_key = api_key
    def main_agent_flow(self):
        # PASS THE API KEY
        agent=langgraph_workflow.WorkflowAgent(self.api_key).langchain_workflow() 
        return agent #returns compiled object

        
if __name__ == "__main__":
    try:
        #How to create a Mongo Db Database
        print('MAIN IS RUNNING.....')
        api_key=get_api_key('GROQ_API_KEY')
        query={'messages': [HumanMessage(content="what is encoder-decoder and explain collections in MongoDb")],
            'topic':'what is encoder-decoder and explain collections in MongoDb',
            'chunks':{
                'mongo_db': [],
                'attn_paper': []
                },
            'task_state' : 'START'}
        flow = AgenticFlow(api_key)
        app=flow.main_agent_flow()
        result=app.invoke(query)
        print('ANSWER:')
        print(result['messages'][-1].content[-1])

    except Exception as e:
        print(e)

#python -m AGENTIC_RAG_MONGODB.main.main
#Expected a Runnable, callable or dict.Instead got an unsupported type: <class 'module'>