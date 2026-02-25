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

    def image(self, prompt: str, image_b64: str):
        payload = {
            "prompt": prompt,
            "image": image_b64
        }

        try:
            response = requests.post(
                f"{self.base_url}/generate-image",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            raise ValueError(f"HF request error: {e}")

        return response.json()