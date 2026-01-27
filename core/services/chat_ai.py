import requests
from django.conf import settings


class HuggingFaceChatService:

    URL = "https://router.huggingface.co/v1/chat/completions"
    MODEL = "HuggingFaceH4/zephyr-7b-beta" 

    @staticmethod
    def ask(question: str) -> str:
        headers = {
            "Authorization": f"Bearer {settings.HF_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {
            "model": HuggingFaceChatService.MODEL,
            "messages": [
                {"role": "user", "content": question}
            ],
            "max_tokens": 300,
            "temperature": 0.7,
            "stream": False
        }

        try:
            response = requests.post(
                HuggingFaceChatService.URL,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(
                    f"HF ERROR {response.status_code}: {response.text}"
                )

            data = response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"HuggingFace request failed: {e}")

        # 🔍 Formato correto da resposta do Router
        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            raise Exception(f"Invalid HF response format: {data}")
