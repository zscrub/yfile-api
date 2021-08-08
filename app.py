import os
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import FileResponse

UPLOAD_DIRECTORY = "uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = FastAPI()

@app.get("/")
async def home():
    return "yfile-api"

@app.get("/files")
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
async def get_file(filename: str):
    # media_type and filename attributes are optional
    return FileResponse(path=UPLOAD_DIRECTORY+'/{0}'.format(filename), headers = {"Content-Disposition": "attachment; filename=" + filename})

#upload a file
@app.post("/files/upload")
async def create_upload_file(file: UploadFile = File(...)):
    if '/' not in file.filename:
        with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
            fp.write(await file.read())
        return 201
    else:
        os.abort(400, 'References to subdirectories not allowed')


if __name__ == "__main__":
    app.run(debug=True, port=8000)