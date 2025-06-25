from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()
index_name = os.getenv("PINECONE_INDEX_NAME")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

if not pc.has_index(index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "chunk_text"}
        }
    )

index = pc.Index(index_name)

class Record: 
    id : str
    text : str

def add_records_to_vector_db(records : list[Record], namespace : str):
    return index.upsert_records(namespace, records)

def query_vector_db(text : str, namespace : str):
    return index.search(
        namespace=namespace,
        query={
            "top_k": 40,
            "inputs": {"text": text}
        }
    )

def describe_index_stats():
    return index.describe_index_stats()

# print(query_vector_db("What is the capital of France?", "expert-agent-knowledge"))

