import fal_client
from django.conf import settings


class ParaFal:
    def __init__(self):
        self.api_key = settings.FAL_API_KEY

    def generate_image(self, prompt):
        print(f"Generating image with FAL for prompt: {prompt[:50]}...")

        result = fal_client.run(
            "fal-ai/nano-banana-2",arguments=
            {
                "prompt": prompt
            },
            headers={
                "Authorization": f"Key {self.api_key}",  
                "Content-Type": "application/json"
            },
        )

        image_url = result["images"][0].get("url")
        return image_url
         