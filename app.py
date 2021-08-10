import os
from json import dump, load
from random import choice
from pydantic import BaseModel
from string import ascii_letters
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, File, UploadFile, HTTPException

UPLOAD_DIRECTORY = "uploaded_files"
password = "password"

with open("db.json", "r") as f:
    JSONtoken = load(f)["token"]

class Auth(BaseModel):
    password: str

class Token(BaseModel):
    token: str


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = FastAPI()

# index
@app.get("/")
async def home():
    return "yfile-api"

# return a list of files from upload_directory
@app.get("/files")
# need to add a token to header
async def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


# download a file 
@app.get("/files/{filename}")
# token needs to be in header
async def get_file(token: Token, filename: str):
    # media_type and filename attributes are optional
    if token.token == JSONtoken:
        return FileResponse(path=UPLOAD_DIRECTORY+'/'+filename, headers = {"Content-Disposition": "attachment; filename="+filename})
    else:
        raise HTTPException(status_code=401, detail="Incorrect token")

# upload a file
@app.post("/files/upload")
# need to pass token in header instead of body (same for other routes)
async def create_upload_file(file: UploadFile = File(...)):
        # if token.token == JSONtoken:
            if '/' not in file.filename:
                with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
                    fp.write(await file.read())
                return 201
            else:
                raise HTTPException(status_code=400, detail='References to subdirectories not allowed')

# route to generate a uuid
@app.post("/token")
def generate_token(login: Auth):
    if login.password == password:
        chars = ascii_letters
        token = ''.join(choice(chars) for _ in range(32)) 
        with open("db.json", "w") as fp:
            dump({"token": token}, fp)
        return token
    else:
        raise HTTPException(status_code=401, detail='Incorrect password')

if __name__ == "__main__":
    app.run(debug=True, port=8000)