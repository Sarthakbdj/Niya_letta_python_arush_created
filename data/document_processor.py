import os
import tempfile
from typing import List, Dict, Any
import PyPDF2
import docx
import tiktoken
import logging
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
        
        # Initialize LangChain text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=self.count_tokens,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX {file_path}: {str(e)}")
            return ""
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read().strip()
            except Exception as e:
                logger.error(f"Error reading TXT file {file_path}: {str(e)}")
                return ""
        except Exception as e:
            logger.error(f"Error extracting text from TXT {file_path}: {str(e)}")
            return ""
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from file based on extension"""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_extension in ['.txt', '.md']:
            return self.extract_text_from_txt(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_extension}")
            return ""
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks using LangChain's RecursiveCharacterTextSplitter
        """
        if not text.strip():
            return []
        
        try:
            # Use LangChain's text splitter to split the text
            chunks = self.text_splitter.split_text(text)
            
            # Process chunks and add metadata
            processed_chunks = []
            for i, chunk_content in enumerate(chunks):
                chunk_token_count = self.count_tokens(chunk_content)
                processed_chunks.append({
                    'content': chunk_content.strip(),
                    'token_count': chunk_token_count,
                    'metadata': metadata or {}
                })
            
            logger.info(f"Split text into {len(processed_chunks)} chunks using LangChain")
            return processed_chunks
            
        except Exception as e:
            logger.error(f"Error chunking text with LangChain: {str(e)}")
            return []
    
    async def process_uploaded_file(self, file_content: bytes, filename: str, 
                                  additional_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Process uploaded file and return chunks ready for vector storage
        """
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name
            
            try:
                # Extract text
                text = self.extract_text_from_file(tmp_file_path)
                
                if not text:
                    logger.warning(f"No text extracted from file: {filename}")
                    return []
                
                # Prepare metadata
                metadata = {
                    'filename': filename,
                    'file_size': len(file_content),
                    'total_text_length': len(text),
                    **(additional_metadata or {})
                }
                
                # Chunk the text
                chunks = self.chunk_text(text, metadata)
                
                # Add source information to each chunk
                processed_chunks = []
                for i, chunk in enumerate(chunks):
                    processed_chunks.append({
                        'content': chunk['content'],
                        'source': filename,
                        'metadata': {
                            **chunk['metadata'],
                            'chunk_index': i,
                            'total_chunks': len(chunks),
                            'token_count': chunk['token_count']
                        }
                    })
                
                logger.info(f"Successfully processed {filename} into {len(processed_chunks)} chunks")
                return processed_chunks
                
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            return []
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions"""
        return ['.pdf', '.docx', '.txt', '.md'] 