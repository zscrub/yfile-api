import os
from json import dump, load
from random import choice
from string import ascii_letters
from typing import Optional

from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel


UPLOAD_DIRECTORY = "uploaded_files"
password = "password"

with open("db.json", "r") as f:
    JSONtoken = load(f)["token"]

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = FastAPI()

# index
@app.get("/")
async def home(token: Optional[str] = Header(None)):
    if token == JSONtoken:
        return "yfile-api"
    else:
        raise HTTPException(status_code=401, detail="Authentication required")

# return a list of files from upload_directory
@app.get("/files")
# need to add a token to header
async def list_files(token: Optional[str] = Header(None)):
    """Endpoint to list files on the server."""
    if token == JSONtoken:
        files = []
        for filename in os.listdir(UPLOAD_DIRECTORY):
            path = os.path.join(UPLOAD_DIRECTORY, filename)
            if os.path.isfile(path):
                files.append(filename)
        return 200, files
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

# download a file 
@app.get("/files/{filename}")
async def get_file(filename: str, token: Optional[str] = Header(None)):
    file_list = (await list_files(token))[1]
    if filename in file_list:
        return FileResponse(path=UPLOAD_DIRECTORY+'/'+filename, headers = {"Content-Disposition": "attachment; filename="+filename})
    else:
        raise HTTPException(status_code=404, detail="File not found")

# upload a file
@app.post("/files/upload")
async def create_upload_file(file: UploadFile = File(...), token: Optional[str] = Header(None)):
        if token == JSONtoken:
            if '/' not in file.filename:
                with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
                    fp.write(await file.read())
                return 201
            else:
                raise HTTPException(status_code=400, detail='References to subdirectories not allowed')
        else:
            raise HTTPException(status_code=401, detail="Invalid token")

@app.delete("/files/delete/{filename}")
async def remove_file(filename: str, token: Optional[str] = Header(None)):
    if token == JSONtoken:
        file_list = (await list_files(token))[1]
        if filename in file_list:
            os.remove(os.path.join(UPLOAD_DIRECTORY, filename))
            return "File {0} deleted".format(filename), 200
        else:
            raise HTTPException(status_code=404, detail="File not found")
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
        
# route to generate a uuid
@app.post("/token")
def generate_token(password_: str):
    if password_ == password:
        chars = ascii_letters
        token = ''.join(choice(chars) for _ in range(32)) 
        with open("db.json", "w") as fp:
            dump({"token": token}, fp)
        return token
    else:
        raise HTTPException(status_code=401, detail='Incorrect password')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
