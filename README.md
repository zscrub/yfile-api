# yfile-api

## Purpose
yfile-api is intended for a user to upload and download files from a specified directory via API calls.

## Routes
> http://127.0.0.1:8000/files

On an accepted request, returns a list with the response code as the first element and a list of existing files within the specified directory. 

An example of a successful response:
```
[
    200,
    [
        "db.db",
        "file.txt"
    ]
]
```

## Example code
### Python
> Get list of files
```py
import requests

url = "http://127.0.0.1:8000/files"

payload={}
headers = {
  'token': 'token_value'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```