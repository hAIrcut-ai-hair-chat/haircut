import requests

response = requests.get("http://127.0.0.1:19003/api/feed/")

print(response.status_code)
print(response.json())
