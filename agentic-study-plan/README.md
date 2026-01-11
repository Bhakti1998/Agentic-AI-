# Agentic-AI-
# AI_Agent_Study_Plan:
An agentic AI system that autonomously generates personalized study plans using LangGraph, LangChain, and ChatGroq.  
The system employs multiple collaborating agents to plan, retrieve, and summarize content efficiently.

---

# Architecture
User → Supervisor Agent → Planner → Retriever → Summarizer → Output

# Overview
1. This project demonstrates a multi-agent workflow managed by a central Supervisor Agent that intelligently delegates tasks to specialized sub-agents.
2. If the user asks for a simple study plan based on a topic , the workflow will run from Supervisor -> planner -> summarizer
3. If the user asks for a study plan based on a topic along with some real time updated study materials and links , the workflow will run from :
   Supervisor -> planner -> retriever -> summarizer
4. The Supervisor is an intelligent entity powered by GROQ LLM , to choose the workflow path based on the user's requirements.     



# Workflow:
1. Supervisor Agent – routes tasks based on the current `task_state`.
2. Planner Agent – generates a step-by-step study plan.
3. Retriever Agent – fetches real-time learning resources using Tavily API.
4. Summarizer Agent – refines and summarizes the final plan.

---

# Features
Dynamic agent orchestration using LangGraph’s StateGraph  
Contextual study plan generation powered by ChatGroq LLM  
Real-time resource retrieval via Tavily Search API  
Concise summarization of study content  
Modular and extendable agent architecture  



