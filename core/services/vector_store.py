import os
from django.conf import settings
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import Chroma
from langchain.schema import Document as LangchainDocument
import logging

from .gemini_service import GeminiService

logger = logging.getLogger(__name__)

class VectorStoreService:
    
    def __init__(self):
        self.config = settings.VECTOR_STORE_CONFIG
        self.gemini_service = GeminiService()
        
        os.makedirs(self.config['PERSIST_DIRECTORY'], exist_ok=True)
        
        self.vector_store = Chroma(
            persist_directory=self.config['PERSIST_DIRECTORY'],
            embedding_function=self.gemini_service.embeddings,
            collection_name=self.config['CHROMA_COLLECTION_NAME']
        )
    
    def add_documents(self, documents: List[LangchainDocument], 
                     metadatas: Optional[List[Dict]] = None) -> List[str]:
        try:
            doc_ids = self.vector_store.add_documents(
                documents=documents,
                metadatas=metadatas
            )
            self.vector_store.persist()
            return doc_ids
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def similarity_search(self, query: str, k: int = None, 
                         filter_dict: Optional[Dict] = None) -> List[LangchainDocument]:
        k = k or self.config['SEARCH_K']
        
        try:
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter_dict
            )
            return results
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = None,
                                   score_threshold: float = None) -> List[tuple]:
        k = k or self.config['SEARCH_K']
        score_threshold = score_threshold or self.config['SCORE_THRESHOLD']
        
        try:
            results = self.vector_store.similarity_search_with_relevance_scores(
                query=query,
                k=k
            )
            return [(doc, score) for doc, score in results if score >= score_threshold]
        except Exception as e:
            logger.error(f"Search with score error: {str(e)}")
            return []
    
    def delete_by_metadata(self, filter_dict: Dict) -> bool:
        try:
            all_docs = self.vector_store.get()
            ids_to_delete = []
            
            for i, metadata in enumerate(all_docs['metadatas']):
                if self._metadata_matches(metadata, filter_dict):
                    ids_to_delete.append(all_docs['ids'][i])
            
            if ids_to_delete:
                self.vector_store.delete(ids=ids_to_delete)
                self.vector_store.persist()
            
            return True
        except Exception as e:
            logger.error(f"Delete error: {str(e)}")
            return False
    
    def _metadata_matches(self, metadata: Dict, filter_dict: Dict) -> bool:
        for key, value in filter_dict.items():
            if metadata.get(key) != value:
                return False
        return True
    
    def get_document_count(self) -> int:
        try:
            return self.vector_store._collection.count()
        except:
            return 0
    
    def clear_all(self) -> bool:
        try:
            self.vector_store.delete_collection()
            self.vector_store = Chroma(
                persist_directory=self.config['PERSIST_DIRECTORY'],
                embedding_function=self.gemini_service.embeddings,
                collection_name=self.config['CHROMA_COLLECTION_NAME']
            )
            return True
        except Exception as e:
            logger.error(f"Clear error: {str(e)}")
            return False
