import requests

response = requests.post(
    "http://127.0.0.1:5001/books",
    json={"name": "Shark"}
)

print(response.text)
