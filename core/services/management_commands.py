import re
import json
from typing import List, Dict, Any
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class RAGUtils:

    @staticmethod
    def save_uploaded_file(file, user_id: str) -> str:
        fs = FileSystemStorage(location=settings.DOCUMENT_CONFIG['UPLOAD_DIR'])
        user_dir = os.path.join(settings.DOCUMENT_CONFIG['UPLOAD_DIR'], str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        filename = fs.save(os.path.join(str(user_id), file.name), file)
        return fs.path(filename)

    @staticmethod
    def extract_file_metadata(file_path: str) -> Dict[str, Any]:
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
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)
        return text.strip()

    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)

    @staticmethod
    def validate_file_type(filename: str) -> bool:
        valid_extensions = ['.pdf', '.txt', '.csv', '.md', '.html']
        ext = os.path.splitext(filename)[1].lower()
        return ext in valid_extensions

    @staticmethod
    def format_response_for_api(response: Dict[str, Any]) -> Dict[str, Any]:
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
