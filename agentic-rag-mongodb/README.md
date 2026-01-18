# Agentic RAG System with MongoDB Vector Search
1. An agentic Retrieval-Augmented Generation (RAG) system that uses planning, tool routing, verification, and replanning to answer domain-specific questions.
2. The domains specified here are MONGO DB basic concepts documentation on tutorials point : https://www.tutorialspoint.com/mongodb/mongodb_tutorial.pdf and Paper for “Attention Is All You Need” (Transformer) Research Paper : https://arxiv.org/pdf/1706.03762.
3. The system supports domain knowledge sources and try to reduce hallucinations through a verifier-driven feedback loop.
4. The LLM Stack used in this project is GROQ Large Language Models

  
# OVERVIEW
This project implements an agentic Retrieval-Augmented Generation (RAG) system with a strong emphasis on deterministic control, inspectable decision-making, and failure-aware replanning. Unlike prompt-heavy or fully autonomous agent designs, this system explicitly separates planning, retrieval, verification, replanning, and generation into well-defined stages.

The primary goal is to explore how hybrid deterministic + LLM-driven agents can produce more reliable and debuggable behavior when answering complex, multi-topic queries.

1. The vector embeddings are precomputed , chunked into relevant groups and is stored into MongoDB Atlas (Free Tier) using cosine similarity.
2. Since the chunks are precomputed , and is stored safely in Mongo Db clusters , the requirement of computing embeddings eliminates completely.
3. A Planner Agent that breaks down queries and decides which tool to assign to which part of the query.
4. Tools Agent one for each specific domain that fetches relevant chunks using MongoDB Atlas Vector Search.
5. A Verifier Agent checks whether retrieved content sufficiently answers the query
6. The system replans and re-retrieves if verification fails
7. A Generator Agent produces the final answer only after validation
8. This design improves answer reliability, domain correctness, and hallucination control.
9. If the tools are not available for a user query or any potential errors are encountered in the process , then the worflow is terminated safely.

    
   <img width="535" height="579" alt="image" src="https://github.com/user-attachments/assets/ec50dab0-70bc-4b9a-8176-a3f95617340d" />


# Tech Stack
1. LLMs: Groq / Qwen / LLaMA (configurable)
2. Agent Framework: LangGraph / Langchain
3. Vector Store: MongoDB Atlas Vector Search
4. Similarity Metric: Cosine similarity
5. Embeddings: MONGO DB ATLAS (Precomputed)
6. Language: Python (3.12.9)
7. IDE: Cursor

# Limitations & Future Work
1. Similarity thresholds are heuristic and domain-dependent
2. Evaluation is currently qualitative; future work includes structured benchmarks
3. Replanner logic can be extended with learned policies
4. Multi-agent coordination is not yet explored

# Takeaway
This project demonstrates that agentic RAG systems do not need to be fully autonomous to be effective. By enforcing deterministic verification and structured replanning, we can build agents that are more reliable, explainable, and engineer-friendly.

This repository represents an architectural prototype and learning-focused exploration, not a production-ready system.

   

   


