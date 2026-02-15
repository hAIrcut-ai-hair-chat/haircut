from django.conf import settings
import requests

class PotasKwenAi:
    def __init__(self):

        self.base_url = settings.HF_BASE_URL
        self.token = settings.HF_TOKEN

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
    def root(self) -> dict:
        
        try:
            response = requests.get(self.base_url, headers=self.headers)
        except Exception as error:
            raise ValueError(f"There's a error in method root in chat hf ai: {error}")
        
        return {
            "message": "HF gguf root endpoint response",
            "json": response.json(),
            "status_code": response.status_code
        }
        
    def generate(self, prompt: str) -> dict:
        
        try:
            response = requests.post(f"{self.base_url}/generate", headers=self.headers, json={"prompt": prompt})
        except Exception as error:
            raise ValueError(f"There's a error in method chat in chat hf ai: {error}")
        
        return {
            "message": "HF gguf root endpoint response",
            "json": response.json(),
            "status_code": response.status_code
        }
        