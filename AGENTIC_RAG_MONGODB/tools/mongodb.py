from AGENTIC_RAG_MONGODB.tools.clean_text import clean_text
from AGENTIC_RAG_MONGODB.embeddings.transformers import get_embedding
from AGENTIC_RAG_MONGODB.collections.MONGO_COLLECTIONS import get_collections
from langchain.tools import tool



tool_schema = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},    
    },
    "required": ["query"]
}

@tool(args_schema=tool_schema)
def get_results_mongo(query:str)-> list:
    """ 
    This tool should be used for answering any questions or performing tasks related to MongoDB concepts or operations. 
    It covers all the main topics from the MongoDB Tutorialspoint PDF, including database creation, collections, 
    CRUD operations, indexing, aggregation, replication, sharding, and backup.
    Call this tool whenever the question involves MongoDB administration, commands, or concepts.
    The tool can help with Retrieving information based on the following topics for MONGO DB:

    1.MongoDB overview, features, advantages , collections , Document
    2.MongoDB environment setup and usage and installation
      1.Install MongoDB on Windows
      2.Install MongoDB on Ubuntu
      3.Start MongoDB
      4.Stop MongoDB
      5.Restart MongoDB
      6.MongoDB Help
      7.MongoDB Statistics

    3.Data modeling and MongoDB datatypes
     1.considerations while designing Schema in MongoDB
    4.Create and drop databases in Mongo Db
    5.Create collections in Mongo Db
    6.MongoDB Advantages 
      1.Advantages of MongoDB over RDBMS
      2.Why Use MongoDB?
      3.Where to Use MongoDB?

    Do NOT use this tool for:

    1.SQL databases
    2.general programming questions
    3.other NoSQL systems (Cassandra, Redis, etc.) """
    
    query_embedding = get_embedding(query)  

    pipeline = [
        {
                "$vectorSearch": {
                "index": "MONGODB_VEC",
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
                "summary": 1,
                "text": 1,
                "source": 1,
                "metadata": 1,
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
    for doc in results:
      array_of_results.append(doc)

    txt=[]
    for tx in array_of_results:
        txt.append((tx['score'],clean_text(tx['text'])))

    

    return txt