import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key(key_name: str) -> str:
    api_key = os.getenv(key_name)

    if not api_key:
        raise ValueError(
            f"Environment variable '{key_name}' not found or is empty."
        )

    return api_key

# if __name__ == "__main__":
#     logger = get_api_key('GROQ_API_KEY')
#     print(logger)

#python -m AGENTIC_RAG_MODULAR.api.api_key