from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import datetime
from uuid import uuid4
qdrant_client = QdrantClient(
    url="http://localhost:6333"
)

COLLECTION_NAME = "memories"
EMBEDDING_DIMENSION = 768

if not qdrant_client.collection_exists(COLLECTION_NAME):
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIMENSION,
            distance=Distance.COSINE,
        ),
    )

load_dotenv("my_assistant/.env")

gemini_client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

EMBEDDING_MODEL = "gemini-embedding-2"

def create_embedding(text: str) -> list[float]:
    result = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    return result.embeddings[0].values

def save_memory(
    text: str,
    memory_type: str = "general",
    metadata: dict | None = None,
) -> str:
    embedding = create_embedding(text)

    point_id = str(uuid4())

    payload = {
        "text": text,
        "type": memory_type,
        "created_at": datetime.now().astimezone().isoformat(),
        "metadata": metadata or {},
    }

    point = PointStruct(
        id=point_id,
        vector=embedding,
        payload=payload,
    )

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point],
    )

    return point_id

def search_memory(query: str, limit: int = 10):
    query_embedding = create_embedding(query)

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
    ).points

    return results

def erase_all_memories():
    qdrant_client.delete_collection(COLLECTION_NAME)

    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIMENSION,
            distance=Distance.COSINE,
        ),
    )