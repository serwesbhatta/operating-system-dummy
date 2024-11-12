from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import uvicorn
from datetime import datetime

# Builtin libraries
import os, sys

# Add the parent directory to the system path to import 'database'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Classes from your module
from database import SqliteCRUD

# import different routes as modules
from routes import *

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

dbFilePath = os.path.join(dataPath, dbName)
print("Checking for database at:", dbFilePath)

if os.path.exists(dbFilePath):
    fsDB = SqliteCRUD(dbFilePath)
    
else:
    fsDB = None
    print("Database file not found.")

# API Routes
@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")

@app.get("/columnNames")
async def get_column_names(table_name: str):
    return await Get_column_names(fsDB, table_name)

@app.get("/files")
async def get_files_route(oid: int, pid: int, name = None):
    return await Get_files(fsDB, oid, pid, name)


@app.post("/touch")
def create_file_route(oid: int, pid: int, name: str):
    return Create_file(fsDB, oid, pid, name)


@app.delete("/rm")
def delete_file_route(oid: int, pid: int, filename: str):
    return Delete_file(fsDB, oid, pid, filename)


@app.get("/file")
def read_file_content(oid: int, pid: int, filename: str):
    return Read_file(fsDB, oid, pid, filename)


@app.post("/filePath")
def write_file_route(oid: int, pid: int, filepath: str, content: str, ):
    return Write_file(fsDB, oid, pid, filepath, content)


@app.put("/mv")
def rename_file_route(oid: int, old_pid: int, old_filename: str, new_pid: int, new_filename: str):
    return Rename_file(fsDB, oid, old_pid, old_filename, new_pid, new_filename)


@app.post("/dir")
def create_directory(oid: int, pid: int, directory_name: str):
    return Create_directory(fsDB, oid, pid, directory_name)

@app.delete("/dir")
def delete_directory(oid: int, pid: int, directory_name: str):
    return Delete_directory(fsDB, oid, pid, directory_name)


@app.get("/dirs")
def list_directories(oid: int, pid: int):
    return List_directories(fsDB, oid, pid)

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)