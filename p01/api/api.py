from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import uvicorn
from datetime import datetime

# Builtin libraries
import os

# Classes from your module
from database.sqliteCRUD import SqliteCRUD

# import different routes as modules
from api.routes import *

# Load environment variables from .env file
load_dotenv()

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# FastAPI application instance
description = """🚀
## File System API (Simulated using SQLite)
"""

app = FastAPI(
    title="File System",
    description=description,
    version="0.0.1",
    terms_of_service="https://serwes.com/terms/",
    contact={
        "name": "FileSystemAPI",
        "url": "https://serwes.com/contact/",
        "email": "chacha@serwes.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Database setup
dataPath = os.getenv("DB_PATH")
dbName = os.getenv("DB_NAME")
if os.path.exists(os.path.join(dataPath, dbName)):
    fsDB = SqliteCRUD(os.path.join(dataPath, dbName))
else:
    fsDB = None
    print("Database file not found.")

# API Routes
@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")

@app.get("/files/")
async def get_files_route(name: str = None):
    return get_files(fsDB, name)


@app.post("/touch")
def create_file_route(name: str):
    return create_file(fsDB, name)


@app.delete("/rm")
def delete_file_route(filename: str):
    return delete_file(fsDB, filename)


@app.get("/file")
def read_file_route(filename: str, user_id: int):
    return read_file(fsDB, filename, user_id)


@app.post("/filePath")
def write_file_route(filepath: str, content: str, user_id: int):
    return write_file(fsDB, filepath, content, user_id)


@app.put("/mv")
def rename_file_route(old_filename: str, new_filename: str):
    return rename_file(fsDB, old_filename, new_filename)


@app.post("/dir")
def create_directory_route(directory_name: str):
    return create_directory(fsDB, directory_name)


@app.delete("/dir")
def delete_directory_route(directory_name: str):
    return delete_directory(fsDB, directory_name)

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)