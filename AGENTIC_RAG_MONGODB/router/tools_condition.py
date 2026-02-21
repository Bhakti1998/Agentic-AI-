#CREATE TOOLS CONDITION FOR ROUTING
from AGENTIC_RAG_MONGODB.state.AgentState import AgentState
def tools_condition(state:AgentState):
    
    status = state['messages'][-1].content[-1]
    rs_lst=status.split('\n')
    fin=[y.replace('"','') for y in rs_lst]
    fin_lst=[x.split(':') for x in fin ]

    vals=[]
    for x in range(len(fin_lst)):
        vals.append(fin_lst[x][2].strip(" ").strip("'"))
    
    # print(vals,status)
    if 'get_results_mongo' in vals:
        return 'MONGODB_TOOL'

    elif 'get_query_results_attn' in vals:
        return 'ATTENTION_TOOL'
        
    else:
        print('No Details Available ... Ending the Process')
        return 'DONE'

