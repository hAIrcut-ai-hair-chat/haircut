import requests
from django.conf import settings


class HuggingFaceChatService:
    
    @staticmethod
    def ask(question: str) -> str:
        payload = {
            "inputs": f"<s>[INST] {question} [/INST]"
        }
        
        headers = {
            "Authorization": f"Bearer {settings.HF_TOKEN}"
        }
        
        response = requests.post(
            settings.HF_AI_MODEL,
            headers=headers,
            json=payload,
            timeout=60
        )
        if response.status_code != 200:
            raise Exception(f"HuggingFace Error: {response.text}")
        
        data = response.json()
        
        if isinstance(data, list):
            return data[0]["generated_text"]
        
        return {"message": "Model didn't return a valid response"}