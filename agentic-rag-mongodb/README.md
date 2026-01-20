# Agentic RAG System with MongoDB Vector Search
# Overview

This project implements an agentic Retrieval-Augmented Generation (RAG) system focused on reliability, inspectability, and controlled execution.
Unlike prompt-heavy or fully autonomous agent designs, the system explicitly separates planning, retrieval, verification, replanning, and generation into deterministic stages.

The system answers domain-specific technical questions using curated knowledge sources while minimizing hallucinations through a verifier-driven feedback loop.

# Problem Statement
Traditional RAG pipelines often:
1. Retrieve irrelevant context
2. Generate answers without validation
3. Fail silently when retrieval quality is low
4. This project explores how hybrid deterministic + LLM-driven agents can improve correctness and debuggability in multi-domain technical QA systems.

# Architecture
# Agent Flow:

Planner Agent:
1. Breaks user queries into sub-tasks / sub-queries
2. Determines which domain tools should be invoked
3. Maps each sub-query to it's particular tool Domain.
4. Returns the steps to be taken for smooth workflow.

Tool Agents:
1. Domain-specific retrievers backed by MongoDB Atlas Vector Search
2. Fetch relevant document chunks using cosine similarity
3. This approach pre-computes all the embeddings for the document chunks , and reduces the cost to re-compute the details again , improving overall latency.
4. Retrival quality can be improved by enabling hybrid search backed by MongoDB Atlas Vector Search.

Verifier Agent: (TRIGGERS REPLANNING )
1. Validates whether retrieved context sufficiently answers the query
2. Triggers replanning and re-retrieval if validation fails
3. Currently the LLM is the core decision maker of the verifier routing , but this can be improved by combining it with more deterministic approaches that strengthens the decision making of the LLM.

Generator Agent:
1. Produces final output only after successful verification.
2. Checks the context thoroughly against the user provided query and provides a summarized final output.

Safe Termination : 
1. Workflow exits cleanly if tools are unavailable or repeated failures occur

# Knowledge Domains:
1. MongoDB Documentation (TutorialsPoint) : https://www.tutorialspoint.com/mongodb/mongodb_tutorial.pdf
2. “Attention Is All You Need” (Transformer research paper) :  https://arxiv.org/pdf/1706.03762 
3. Embeddings are precomputed offline, chunked, and stored in MongoDB Atlas to reduce runtime latency and inference cost.

# LANGGRAPH DIAGRAM:
   <img width="535" height="579" alt="image" src="https://github.com/user-attachments/assets/ec50dab0-70bc-4b9a-8176-a3f95617340d" />

# Tech Stack:
1. LLMs: Groq / Qwen / LLaMA (configurable)
2. Agent Framework: LangGraph, LangChain
3. Vector Store: MongoDB Atlas Vector Search
4. Similarity Metric: Cosine similarity
5. Language: Python 3.12.10
6. IDE: Cursor

# Key Design Decisions
1. Deterministic agent orchestration instead of fully autonomous agents
2. Explicit verification before generation
3. Failure-aware replanning loops
4. Precomputed embeddings for predictable performance

# Limitations & Future Work
1. Similarity thresholds are heuristic and domain-specific
2. Evaluation is currently qualitative
3. Replanning logic can be extended using learned policies
4. Multi-agent collaboration patterns are not yet implemented

# Takeaway
This project demonstrates that agentic RAG systems do not need full autonomy to be effective.
Structured planning, verification, and controlled replanning can significantly improve reliability, explainability, and engineering confidence.

