# Agentic RAG System with MongoDB Vector Search
1. An agentic Retrieval-Augmented Generation (RAG) system that uses planning, tool routing, verification, and replanning to answer domain-specific questions.
2. The domains specified here are MONGO DB basic concepts documentation on tutorials point : https://www.tutorialspoint.com/mongodb/mongodb_tutorial.pdf and Paper for “Attention Is All You Need” (Transformer) Research Paper : https://arxiv.org/pdf/1706.03762.
3. The system supports domain knowledge sources and try to reduce hallucinations through a verifier-driven feedback loop.
4. The LLM Stack used in this project is GROQ Large Language Models

  
# OVERVIEW
Traditional RAG pipelines follow a linear flow: retrieve → generate.
This project goes beyond that by implementing an agentic architecture where:

1. A Planner Agent that breaks down queries and decides which tool to assign to which part of the query
2  Tools Agent one for each specific domain that fetches relevant chunks using MongoDB Atlas Vector Search
3. A Verifier Agent checks whether retrieved content sufficiently answers the query
4. The system replans and re-retrieves if verification fails
5. A Generator Agent produces the final answer only after validation
6. This design improves answer reliability, domain correctness, and hallucination control.
7. If the tools are not available of any potential errors are encountered in the process , then the worflow is terminated safely
   <img width="535" height="579" alt="image" src="https://github.com/user-attachments/assets/ec50dab0-70bc-4b9a-8176-a3f95617340d" />

# Tech Stack

1. LLMs: Groq / Qwen / LLaMA (configurable)
2. Agent Framework: LangGraph / Langchain
3. Vector Store: MongoDB Atlas Vector Search
4. Similarity Metric: Cosine similarity
5. Embeddings: Precomputed offline
6. Language: Python
7. IDE: Cursor

   


