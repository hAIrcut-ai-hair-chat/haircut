import requests

url = "http://localhost:8000/api/image/"

with open("code.jpeg", "rb") as img:
    files = {
        "file": ("code.jpeg", img, "image/jpeg")  # 🔥 AQUI mudou de image → file
    }

    response = requests.post(url, files=files)

print(response.status_code)

try:
    print(response.json())
except Exception:
    print(response.text)