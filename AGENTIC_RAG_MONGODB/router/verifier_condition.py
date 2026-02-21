from AGENTIC_RAG_MONGODB.state.AgentState import AgentState

def verifier_condition(state:AgentState):
    state=state['task_state']
        
    if 'VERIFICATION DONE' in state:
        print("--- VERIFICATION COMPLETED  ---")
        return 'GENERATE'

    elif 'MAKE_ANOTHER_TOOL_CALL' in state:
        
        print("--- DATA INSUFFICIENT RE-PLANNING  ---")
        return 'REPLAN'

    else:
        print("--- UNKNOWN STATUS . STOPPING PROCESS  ---")
        return 'DONE'