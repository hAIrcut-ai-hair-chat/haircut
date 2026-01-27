import os
import hashlib
from typing import List, Dict, Any
from django.conf import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredMarkdownLoader,
    WebBaseLoader
)
from langchain.schema import Document as LangchainDocument
import logging

from .vector_store import VectorStoreService

logger = logging.getLogger(__name__)

class DocumentProcessor:
    
    def __init__(self):
        self.config = settings.VECTOR_STORE_CONFIG
        self.vector_store = VectorStoreService()
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config['CHUNK_SIZE'],
            chunk_overlap=self.config['CHUNK_OVERLAP'],
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_document(self, file_path: str, file_type: str, 
                        metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            loader = self._get_loader(file_path, file_type)
            documents = loader.load()
            
            chunks = self.text_splitter.split_documents(documents)
            
            enhanced_chunks = []
            for i, chunk in enumerate(chunks):
                chunk_metadata = chunk.metadata.copy() if chunk.metadata else {}
                chunk_metadata.update({
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'source_file': os.path.basename(file_path),
                    'file_type': file_type,
                    'chunk_hash': self._generate_hash(chunk.page_content)
                })
                
                if metadata:
                    chunk_metadata.update(metadata)
                
                enhanced_chunk = LangchainDocument(
                    page_content=chunk.page_content,
                    metadata=chunk_metadata
                )
                enhanced_chunks.append(enhanced_chunk)
            
            doc_ids = self.vector_store.add_documents(enhanced_chunks)
            
            return {
                'success': True,
                'document_count': len(documents),
                'chunk_count': len(chunks),
                'doc_ids': doc_ids
            }
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_text(self, text: str, source_name: str = "text_input",
                    metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            document = LangchainDocument(
                page_content=text,
                metadata=metadata or {}
            )
            
            chunks = self.text_splitter.split_documents([document])
            
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'source_name': source_name,
                    'chunk_hash': self._generate_hash(chunk.page_content)
                })
            
            doc_ids = self.vector_store.add_documents(chunks)
            
            return {
                'success': True,
                'chunk_count': len(chunks),
                'doc_ids': doc_ids
            }
            
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_url(self, url: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            loader = WebBaseLoader([url])
            documents = loader.load()
            
            chunks = self.text_splitter.split_documents(documents)
            
            for i, chunk in enumerate(chunks):
                chunk_metadata = chunk.metadata.copy() if chunk.metadata else {}
                chunk_metadata.update({
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'source_url': url,
                    'chunk_hash': self._generate_hash(chunk.page_content)
                })
                
                if metadata:
                    chunk_metadata.update(metadata)
                
                chunk.metadata = chunk_metadata
            
            doc_ids = self.vector_store.add_documents(chunks)
            
            return {
                'success': True,
                'chunk_count': len(chunks),
                'doc_ids': doc_ids
            }
            
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_loader(self, file_path: str, file_type: str):
        loaders = {
            'pdf': PyPDFLoader,
            'txt': TextLoader,
            'csv': CSVLoader,
            'md': UnstructuredMarkdownLoader,
        }
        
        if file_type not in loaders:
            raise ValueError(f"Unsupported type: {file_type}")
        
        return loaders[file_type](file_path)
    
    def _generate_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()[:32]
    
    def get_supported_formats(self) -> List[str]:
        return ['pdf', 'txt', 'csv', 'md', 'url']
