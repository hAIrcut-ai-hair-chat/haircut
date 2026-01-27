import re
import json
from typing import List, Dict, Any
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

class RAGUtils:
    """Utilitários para o sistema RAG"""
    
    @staticmethod
    def save_uploaded_file(file, user_id: str) -> str:
        """Salva arquivo enviado e retorna caminho"""
        fs = FileSystemStorage(location=settings.DOCUMENT_CONFIG['UPLOAD_DIR'])
        
        # Cria diretório do usuário
        user_dir = os.path.join(settings.DOCUMENT_CONFIG['UPLOAD_DIR'], str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        # Salva arquivo
        filename = fs.save(os.path.join(str(user_id), file.name), file)
        return fs.path(filename)
    
    @staticmethod
    def extract_file_metadata(file_path: str) -> Dict[str, Any]:
        """Extrai metadados do arquivo"""
        import os
        
        stats = os.stat(file_path)
        
        return {
            'file_size': stats.st_size,
            'created_at': stats.st_ctime,
            'modified_at': stats.st_mtime,
            'file_name': os.path.basename(file_path),
            'file_extension': os.path.splitext(file_path)[1].lower()
        }
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Limpa texto removendo caracteres especiais"""
        # Remove múltiplos espaços
        text = re.sub(r'\s+', ' ', text)
        # Remove caracteres de controle
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)
        return text.strip()
    
    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """Divide texto em frases"""
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)
    
    @staticmethod
    def validate_file_type(filename: str) -> bool:
        """Valida tipo de arquivo"""
        valid_extensions = ['.pdf', '.txt', '.csv', '.md', '.html']
        ext = os.path.splitext(filename)[1].lower()
        return ext in valid_extensions
    
    @staticmethod
    def format_response_for_api(response: Dict[str, Any]) -> Dict[str, Any]:
        """Formata resposta para API"""
        return {
            'data': {
                'answer': response.get('answer', ''),
                'sources': response.get('sources', []),
                'metadata': response.get('metadata', {})
            },
            'success': response.get('success', False),
            'error': response.get('error'),
            'performance': {
                'response_time': response.get('response_time', 0),
                'tokens_used': response.get('tokens_used', 0)
            }
        }