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
    return Get_files(fsDB, name)


@app.post("/touch")
def create_file_route(name: str):
    return Create_file(fsDB, name)


@app.delete("/rm")
def delete_file_route(filename: str):
    return Delete_file(fsDB, filename)


@app.get("/file")
def read_file_route(filename: str, user_id: int):
    return Read_file(fsDB, filename, user_id)


@app.post("/filePath")
def write_file_route(filepath: str, content: str, user_id: int):
    return Write_file(fsDB, filepath, content, user_id)


@app.put("/mv")
def rename_file_route(old_filename: str, new_filename: str):
    return Rename_file(fsDB, old_filename, new_filename)


@app.post("/dir")
def create_directory(directory_name: str):
    """
    Create a new directory in the simulated filesystem and log the action in the database.
    :param directory_name: The name of the new directory.
    """
    if fsDB:
        # Check if the directory already exists
        parent = 1
        filters = {"name": directory_name, "pid": parent}  # Assuming root directory
        existing_dir = fsDB.read_data("directories", filters)
         
        if existing_dir:
            raise HTTPException(status_code=400, detail="Directory already exists.")
        
        # Insert the new directory into the database
        fsDB.insert_data(
            "directories", (None, parent, None, directory_name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
            1, 0, 1, 1, 0, 1)  # Permissions and default values
        )
        
        return {"message": f"Directory '{directory_name}' created successfully."}
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")



@app.delete("/dir")
def delete_directory(directory_name: str):
    """
    Delete a directory and its contents from the simulated filesystem (database) and log the action.
    :param directory_name: The name of the directory to be deleted.
    """
    if fsDB:
        # Check if the directory exists in the database
        filters = {"name": directory_name, "pid": 1}  # Assuming root directory
        directory_record = fsDB.read_data("directories", filters)
        
        if directory_record:
            # Delete the directory from the database
            fsDB.delete_data("directories", "name", directory_name)
            return {"message": f"Directory '{directory_name}' deleted from the database."}
        else:
            raise HTTPException(status_code=404, detail="Directory not found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.get("/dirs")
def list_directories(parent: int = 1):
    """
    List all directories under a specific parent directory in the simulated filesystem.
    :param parent_id: The ID of the parent directory (default is root directory with ID 1).
    """
    if fsDB:
        # Fetch directories under the specified parent directory
        filters = {"pid": parent}  # pid represents parent directory ID
        directories = fsDB.read_data("directories", filters)
        
        if directories:
            return {"directories": directories}
        else:
            raise HTTPException(status_code=404, detail="No directories found under the specified parent directory.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)