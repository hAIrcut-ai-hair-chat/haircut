from typing import List, Dict, Any
from django.core.cache import cache
import json
from time import time
class ConversationMemory:
    
    def __init__(self, user_id: str, conversation_id: str = None):
        self.user_id = user_id
        self.conversation_id = conversation_id or f"conv_{user_id}"
        self.cache_key = f"conversation:{self.conversation_id}"
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        conversation = self.get_conversation()
        
        message = {
            'role': role,
            'content': content,
            'timestamp': time.time(),
            'metadata': metadata or {}
        }
        
        conversation['messages'].append(message)
        conversation['updated_at'] = time.time()
        
        cache.set(self.cache_key, json.dumps(conversation), 86400)
    
    def get_conversation(self) -> Dict[str, Any]:
        cached = cache.get(self.cache_key)
        if cached:
            return json.loads(cached)
        
        return {
            'user_id': self.user_id,
            'conversation_id': self.conversation_id,
            'created_at': time.time(),
            'updated_at': time.time(),
            'messages': []
        }
    
    def get_last_messages(self, n: int = 5) -> List[Dict]:
        conversation = self.get_conversation()
        return conversation['messages'][-n:]
    
    def clear(self):
        cache.delete(self.cache_key)
    
    def get_summary(self) -> str:
        conversation = self.get_conversation()
        messages = conversation['messages']
        
        if not messages:
            return "Empty conversation"
        
        summary = f"Conversation with {len(messages)} messages:\n"
        for msg in messages[-3:]:
            summary += f"{msg['role']}: {msg['content'][:100]}...\n"
        
        return summary
