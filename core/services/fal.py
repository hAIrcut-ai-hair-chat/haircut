import fal_client
from django.conf import settings

class ParaFAl:
    def __init__(self):
        self.client = fal_client.Client(api_key=settings.FAL_API_KEY)

    def generate_image(self, prompt):
        response = self.client.run(
            "fal-ai/dall-e-3",
            arguments={
                "prompt": prompt,
                "size": "1024x1024",
                "quality": "standard",
            }
        )
        return response.get("images", [])[0].get("url")