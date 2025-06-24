# import pineconedb as vectors

# print(vectors.query_vector_db("What is the capital of France?", "expert-agent-knowledge"))

import document_processor as dp
import asyncio
import json

a = asyncio.run(dp.DocumentProcessor().process_uploaded_file(file_content=open("heythere.txt", "rb").read(), filename="heythere.txt"))

print(a[0]["metadata"])





