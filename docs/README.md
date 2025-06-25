# Expert Agent with Pinecone Vector Search

A powerful AI agent that learns from uploaded documents using Pinecone vector search and OpenAI embeddings. Upload documents to expand the agent's knowledge base and ask questions to get intelligent, context-aware answers.

## Features

- **Document Upload & Processing**: Support for PDF, DOCX, TXT, and Markdown files
- **Vector Search**: Powered by Pinecone for fast and accurate document retrieval
- **Smart Chunking**: Intelligent text chunking with overlap for better context preservation
- **Expert AI Agent**: GPT-4 powered agent that provides comprehensive answers with source citations
- **RESTful API**: Clean FastAPI-based API for easy integration
- **Conversation Support**: Maintain context across multiple questions
- **Knowledge Base Management**: View stats, search directly, and manage documents by source

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key
- Pinecone API key and environment

### Installation

1. **Clone and navigate to the project:**
```bash
cd python-ai-backend
```

2. **Create and activate virtual environment:**
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
PINECONE_INDEX_NAME=expert-agent-knowledge
EMBEDDING_MODEL=text-embedding-ada-002
```

### Getting API Keys

#### OpenAI API Key
1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key to your `.env` file

#### Pinecone Setup
1. Sign up at [Pinecone](https://www.pinecone.io/)
2. Create a new project
3. Go to API Keys section
4. Copy your API key and environment name
5. The index will be created automatically when you start the application

## Usage

### Starting the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints

#### 1. Upload Documents
```bash
POST /upload
```

Upload a document to expand the agent's knowledge base:

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

#### 2. Ask Questions
```bash
POST /ask
```

Ask the expert agent a question:

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main findings in the research?",
    "top_k": 5
  }'
```

#### 3. Chat Conversation
```bash
POST /chat
```

Have a conversation with context:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is machine learning?"},
      {"role": "assistant", "content": "Machine learning is..."},
      {"role": "user", "content": "Can you give me specific examples?"}
    ]
  }'
```

#### 4. Knowledge Base Stats
```bash
GET /knowledge-base/stats
```

Get information about your knowledge base:

```bash
curl -X GET "http://localhost:8000/knowledge-base/stats"
```

#### 5. Search Knowledge Base
```bash
GET /search?query=your_search_term&top_k=5
```

Search directly in the knowledge base:

```bash
curl -X GET "http://localhost:8000/search?query=machine%20learning&top_k=5"
```

#### 6. Delete Documents by Source
```bash
DELETE /knowledge-base/source/{source_name}
```

Remove all documents from a specific source:

```bash
curl -X DELETE "http://localhost:8000/knowledge-base/source/document.pdf"
```

### Python Client Example

```python
import requests
import json

# Upload a document
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload', files=files)
    print(response.json())

# Ask a question
question_data = {
    "question": "What are the key concepts discussed in the document?",
    "top_k": 5
}
response = requests.post('http://localhost:8000/ask', json=question_data)
result = response.json()

print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
print(f"Confidence: {result['confidence']}%")
```

## Supported File Types

- **PDF** (`.pdf`)
- **Word Documents** (`.docx`)
- **Text Files** (`.txt`)
- **Markdown** (`.md`)

## Configuration

### Document Processing
- **Chunk Size**: 1000 tokens (adjustable in `DocumentProcessor`)
- **Chunk Overlap**: 100 tokens
- **Max Context**: 4000 tokens for agent responses

### Vector Search
- **Index Dimension**: 1536 (OpenAI ada-002)
- **Similarity Metric**: Cosine similarity
- **Default Top-K**: 5 most relevant documents

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │ Document         │    │ Pinecone        │
│                 │──→ │ Processor        │──→ │ Vector Store    │
│   /upload       │    │                  │    │                 │
│   /ask          │    │ - PDF/DOCX/TXT   │    │ - Embeddings    │
│   /chat         │    │ - Text Chunking  │    │ - Similarity    │
└─────────────────┘    │ - Tokenization   │    │   Search        │
                       └──────────────────┘    └─────────────────┘
                                │                        │
                       ┌──────────────────┐    ┌─────────────────┐
                       │ OpenAI API       │    │ Expert Agent    │
                       │                  │←───│                 │
                       │ - Embeddings     │    │ - GPT-4         │
                       │ - Chat Completion│    │ - Context Build │
                       └──────────────────┘    │ - Source Citing │
                                               └─────────────────┘
```

## Error Handling

The API provides detailed error messages and proper HTTP status codes:

- `400`: Bad Request (unsupported file type, invalid input)
- `500`: Internal Server Error (API failures, processing errors)

## Performance Considerations

- **File Size**: Large files are processed in chunks
- **Concurrent Uploads**: Multiple files can be uploaded simultaneously
- **Rate Limiting**: Implement rate limiting for production use
- **Caching**: Consider caching frequently asked questions

## Development

### Adding New File Types

1. Extend `DocumentProcessor.extract_text_from_file()`
2. Add the new extension to `get_supported_extensions()`
3. Install necessary parsing libraries

### Customizing the Agent

Modify `ExpertAgent` to:
- Change the system prompt
- Adjust response length
- Modify confidence calculation
- Add custom filters

## Troubleshooting

### Common Issues

1. **Pinecone Connection Errors**
   - Verify API key and environment in `.env`
   - Check if the index exists in your Pinecone console

2. **OpenAI API Errors**
   - Ensure you have sufficient credits
   - Verify the API key is correct

3. **File Processing Errors**
   - Check if the file format is supported
   - Ensure files are not corrupted

4. **Memory Issues**
   - Large files may require chunking optimization
   - Consider reducing chunk size or overlap

### Logs

Check the application logs for detailed error information:
```bash
python main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Create an issue in the repository

---

Built with ❤️ using FastAPI, Pinecone, and OpenAI 