# yfile-api

## Purpose
yfile-api is intended for a user to upload and download files from a specified directory via API calls. 

## Routes
### http://localhost:8000/files
> Get list of files

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

### Python
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

### Go 
```go
package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
)

func main() {

  url := "http://127.0.0.1:8000/files"
  method := "GET"

  client := &http.Client {
  }
  req, err := http.NewRequest(method, url, nil)

  if err != nil {
    fmt.Println(err)
    return
  }
  req.Header.Add("token", "token_value")

  res, err := client.Do(req)
  if err != nil {
    fmt.Println(err)
    return
  }
  defer res.Body.Close()

  body, err := ioutil.ReadAll(res.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(string(body))
}
```
