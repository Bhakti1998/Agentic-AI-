from AGENTIC_RAG_MONGODB.tools.clean_text import clean_text
from AGENTIC_RAG_MONGODB.embeddings.transformers import get_embedding
from AGENTIC_RAG_MONGODB.collections.ATTENTION_PAPER_COLLECTION import get_collections
from langchain.tools import tool



tool_schema = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},    
    },
    "required": ["query"]
}
@tool(args_schema=tool_schema)
def get_query_results_attn(query:str)-> list:
   """Retrieve information based on the following topics.
   1."Attention Is All You Need" paper
   2.Transformer architecture
   3.Self-attention mechanism
   4.Encoder decoder transformers
   5.Original transformer equations """
   
   query_embedding = get_embedding(query)


   pipeline = [
      {
            "$vectorSearch": {
               "index": "ATTN_VEC",
               "queryVector": query_embedding,
               "path": "embedding",
               "exact": False,
               "numCandidates": 100,
               "limit": 50,
               "similarity": "cosine"
            }
      }, {
            "$project": {
               "_id": 0,
               "text": 1,
               "source": 1,
               "metadata": 1,
               "summary": 1,
               "listing_url": 1,
               "score": {
                  "$meta": "vectorSearchScore"
               }
            }
      }
   ]

   collections= get_collections() 
   results = collections.aggregate(pipeline)
   

   array_of_results = []
   # print(results)
   for doc in results:
      array_of_results.append(doc)
      
   
   txt=[]
   for tx in array_of_results:
        txt.append((tx['score'],clean_text(tx['text'])))

    

   return txt