import os
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

UPLOAD_DIRECTORY = "/uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = FastAPI()

@app.get("/")
async def home():
    return "yfile-app"

@app.get("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

@app.get("/files/{filename}")
def get_file(filename: str):
    """Download a file."""
    print(filename)
    print(UPLOAD_DIRECTORY)
    # media_type and filename attributes are optional
    return FileResponse(path=UPLOAD_DIRECTORY, headers = {"Content-Disposition": "attachment; filename=" + filename})

@app.post("/files/upload/<filename>")
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        os.abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(Request.data)

    # Return 201 CREATED
    return "", 201

if __name__ == "__main__":
    app.run(debug=True, port=8000)