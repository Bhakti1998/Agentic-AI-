from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder

#INITIALIZE SENTENCE TRANSFORMERS FOR EMBEDDINGS
model = SentenceTransformer ('BAAI/bge-large-en-v1.5')

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def get_embedding(text):
    embeddings=model.encode(text, batch_size=3 ,normalize_embeddings=True).tolist()
    return embeddings
