# Libraries for FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# Builtin libraries
import os

from random import choice

# Classes from your module
# from module import SqliteCRUD
from database import SqliteCRUD

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# FastAPI application instance
description = """🚀
## File System API
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
dataPath = "../data/"
dbName = "filesystem.db"
if os.path.exists(os.path.join(dataPath, dbName)):
    fsDB = SqliteCRUD(os.path.join(dataPath, dbName))
else:
    fsDB = None
    print("Database file not found.")
  
# Routes

@app.get("/")
async def docs_redirect():
    """Redirect to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/files/")
async def get_files(did=None):
    """
    Get a list of files in the current directory.
    """
    if fsDB:
        files = fsDB.read_data("files")
        if files:
            return files
        else:
            raise HTTPException(status_code=404, detail="No files found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.post("/touch")
def create_file(name: str):
    """
    Create a new file in the filesystem and record the action in the database.
    """
    if fsDB:
        parent = choice([3, 4, 5, 6, 7])
        existing_file = fsDB.read_data("files", name)

        if existing_file:
            raise HTTPException(status_code=400, detail="File already exists.")

        fsDB.insert_data(
            "files", (None, name, parent, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        )
        return {"message": f"File '{name}' created successfully."}
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.delete("/rm")
def delete_file(filepath: str):
    """
    Delete a file from the filesystem and record the action in the database.
    """
    if fsDB:
        if fsDB.read_data("files", filepath):
            try:
                os.remove(filepath)
                fsDB.update_file(filepath, "deleted")
                return {"message": f"File '{filepath}' deleted successfully."}
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="File not found.")
        else:
            raise HTTPException(status_code=404, detail="File not found in database.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.get("/file")
def read_file(filepath: str):
    """
    Read the contents of a file and log the read action in the database.
    """
    if fsDB:
        try:
            with open(filepath, 'r') as file:
                content = file.read()
            fsDB.insert_action(filepath, "read")
            return {"content": content}
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.post("/filePath")
def write_file(filepath: str, content: str):
    """
    Write data to a file and log the write operation in the database.
    """
    if fsDB:
        try:
            with open(filepath, 'w') as file:
                file.write(content)
            fsDB.insert_action(filepath, "written")
            return {"message": f"Content written to {filepath}."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.put("/mv")
def rename_file(old_filepath: str, new_filepath: str):
    """
    Rename a file in the filesystem and update the database with the new name.
    """
    if fsDB:
        try:
            os.rename(old_filepath, new_filepath)
            fsDB.update_filename(old_filepath, new_filepath)
            return {"message": f"File renamed from {old_filepath} to {new_filepath}."}
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.post("/dir")
def create_directory(directory_path: str):
    """
    Create a new directory in the filesystem and log the action in the database.
    """
    if fsDB:
        try:
            os.makedirs(directory_path)
            fsDB.insert_directory(directory_path, "created")
            return {"message": f"Directory '{directory_path}' created successfully."}
        except FileExistsError:
            raise HTTPException(status_code=400, detail="Directory already exists.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.delete("/dir")
def delete_directory(directory_path: str):
    """
    Delete a directory and its contents from the filesystem and log the action in the database.
    """
    if fsDB:
        try:
            os.rmdir(directory_path)
            fsDB.update_directory(directory_path, "deleted")
            return {"message": f"Directory '{directory_path}' deleted successfully."}
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Directory not found.")
        except OSError as e:
            raise HTTPException(status_code=400, detail="Directory is not empty.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)
