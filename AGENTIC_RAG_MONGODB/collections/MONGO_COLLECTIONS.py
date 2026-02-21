from pymongo import MongoClient
from AGENTIC_RAG_MONGODB.api.api_key import get_api_key

def get_collections():
    try:
        mongo_key=get_api_key('MONGO_DB')
        client = MongoClient(f"{mongo_key}")
        if (client.admin.command("ping"))['ok'] == 1:
            print('here')
            return client["sample_mflix"]['MONGODB']

        else:
            print('No connection')
            return 'No connection'

    except Exception as e:
        return e


# if __name__ == "__main__":
#     logger = get_collections('MONGODB')
#     print(logger)

#python -m AGENTIC_RAG_MODULAR.collections.mongodb