import requests

response = requests.delete(
    "http://127.0.0.1:5001/books/5"
)

print(response.status_code)
print(response.text)