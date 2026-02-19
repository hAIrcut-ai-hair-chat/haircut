from django.conf import settings
import requests
import base64

class PotasImageAI:
    def __init__(self):
        self.base_url = settings.HF_BASE_URL
        self.token = settings.HF_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def image(self, prompt: str, image: bytes):
        image_base64 = base64.b64encode(image).decode("utf-8")
        payload = {
            "prompt": prompt,
            "image": image_base64
        }

        try:
            response = requests.post(f"{self.base_url}/image", headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"HF request error: {e}")

        return {
            "message": "HF endpoint response",
            "data": data,
            "status_code": response.status_code
        }
