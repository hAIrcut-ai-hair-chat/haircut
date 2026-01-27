import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from django.conf import settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    
    def __init__(self):
        self.config = settings.GEMINI_CONFIG
        
        if not self.config['API_KEY']:
            raise ValueError("GEMINI_API_KEY is not configured")
        
        genai.configure(api_key=self.config['API_KEY'])
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.config['MODEL_NAME'],
            temperature=self.config['TEMPERATURE'],
            convert_system_message_to_human=True
        )
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=self.config['EMBEDDING_MODEL']
        )
    
    def generate_response(self, prompt: str, context: str = "") -> Dict[str, Any]:
        try:
            full_prompt = self._build_rag_prompt(prompt, context)
            
            response = self.llm.invoke(full_prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            return {
                'success': True,
                'content': content,
                'tokens_used': self._estimate_tokens(content)
            }
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_embedding(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
    
    def batch_embed(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)
    
    def _build_rag_prompt(self, question: str, context: str) -> str:
        if context:
            return f"""
            Provided context:
            {context}
            
            Based on the context above, answer the following question:
            {question}
            
            If the answer is not in the context, say that you do not have this information.
            """
        return question
    
    def _estimate_tokens(self, text: str) -> int:
        return len(text.split()) // 0.75
    
    @staticmethod
    def get_available_models():
        try:
            models = genai.list_models()
            return [
                {
                    'name': model.name,
                    'display_name': model.display_name,
                    'description': model.description
                }
                for model in models
                if 'generateContent' in model.supported_generation_methods
            ]
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return []
