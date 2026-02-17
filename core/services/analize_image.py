from django.conf import settings
import requests

class PotasImageAI:
    def __init__(self):
        self.base_url = settings.HF_BASE_URL
        self.token = settings.HF_TOKEN

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    def image(self, prompt: str, image):
        json_data = {
            "prompt": prompt,
            "image": image
        }
        
        try:
            response = requests.post(f"{self.base_url}/image", headers=self.headers, json=json_data)
        except Exception as error:
            raise ValueError(f"There's a error in method image in hf ai: {error}")
        
        return {
            "message": "HF gguf root endpoint response",
            "json": response.json(),
            "status_code": response.status_code
        }
        