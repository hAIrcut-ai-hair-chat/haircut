import time
from typing import List, Dict, Any
from django.conf import settings
import logging

from .gemini_service import GeminiService
from .vector_store import VectorStoreService

logger = logging.getLogger(__name__)

class RAGService:
    
    def __init__(self):
        self.gemini = GeminiService()
        self.vector_store = VectorStoreService()
        self.config = settings.VECTOR_STORE_CONFIG
    
    def query(self, question: str, k: int = None, 
             score_threshold: float = None,
             filter_dict: Dict = None,
             chat_history: List[Dict] = None) -> Dict[str, Any]:
        
        start_time = time.time()
        
        try:
            relevant_docs = self.vector_store.similarity_search_with_score(
                query=question,
                k=k or self.config['SEARCH_K'],
                score_threshold=score_threshold or self.config['SCORE_THRESHOLD']
            )
            
            if filter_dict:
                relevant_docs = [
                    (doc, score) for doc, score in relevant_docs
                    if self._check_metadata(doc.metadata, filter_dict)
                ]
            
            context = self._build_context(relevant_docs)
            sources = self._extract_sources(relevant_docs)
            
            response = self.gemini.generate_response(
                prompt=question,
                context=context
            )
            
            if not response['success']:
                raise Exception(response.get('error', 'Error generating response'))
            
            response_time = time.time() - start_time
            
            return {
                'success': True,
                'answer': response['content'],
                'sources': sources,
                'context_chunks': len(relevant_docs),
                'response_time': response_time,
                'tokens_used': response.get('tokens_used', 0),
                'metadata': {
                    'question': question,
                    'k': k or self.config['SEARCH_K'],
                    'score_threshold': score_threshold or self.config['SCORE_THRESHOLD']
                }
            }
            
        except Exception as e:
            logger.error(f"RAG query error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'answer': f"Error processing query: {str(e)}"
            }
    
    def batch_query(self, questions: List[str], **kwargs) -> List[Dict[str, Any]]:
        results = []
        
        for question in questions:
            result = self.query(question, **kwargs)
            results.append({
                'question': question,
                **result
            })
        
        return results
    
    def _build_context(self, relevant_docs: List[tuple]) -> str:
        if not relevant_docs:
            return ""
        
        context_parts = []
        for i, (doc, score) in enumerate(relevant_docs):
            context_parts.append(f"[Document {i+1}, Score: {score:.3f}]:\n{doc.page_content}")
        
        return "\n\n".join(context_parts)
    
    def _extract_sources(self, relevant_docs: List[tuple]) -> List[Dict]:
        sources = []
        seen = set()
        
        for doc, score in relevant_docs:
            metadata = doc.metadata
            source_key = metadata.get('source_file') or metadata.get('source_url')
            
            if source_key and source_key not in seen:
                seen.add(source_key)
                sources.append({
                    'source': source_key,
                    'file_type': metadata.get('file_type'),
                    'chunk_index': metadata.get('chunk_index'),
                    'score': float(score)
                })
        
        return sources
    
    def _check_metadata(self, metadata: Dict, filter_dict: Dict) -> bool:
        for key, value in filter_dict.items():
            if metadata.get(key) != value:
                return False
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'document_count': self.vector_store.get_document_count(),
            'config': {
                'chunk_size': self.config['CHUNK_SIZE'],
                'chunk_overlap': self.config['CHUNK_OVERLAP'],
                'search_k': self.config['SEARCH_K'],
                'score_threshold': self.config['SCORE_THRESHOLD']
            }
        }
