from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# Builtin libraries
import os

# Classes from your module
from module import SqliteCRUD

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
dataPath = "./data/"
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
    Get a list of files from the simulated filesystem (from the database).
    """
    filters = {"name": did}
    if fsDB:
        files = fsDB.read_data("files", filters)
        if files:
            return files
        else:
            raise HTTPException(status_code=404, detail="No files found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.post("/touch")
def create_file(name: str):
    """
    Create a new file in the simulated filesystem and record the action in the database.
    """
    if fsDB:
        parent = 1  # Assuming 1 is the root directory ID; update based on the schema
        filters = {'name': name}
        existing_file = fsDB.read_data("files", filters)

        print("Database is initialized")

        if existing_file:
            print("File already exists")
            raise HTTPException(status_code=400, detail="File already exists.")

        print("Inserting Data")
        fsDB.insert_data(
            "files", (None, name, parent, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        )
        
        return {"message": f"File '{name}' created successfully."}
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.delete("/rm")
def delete_file(filename: str):
    """
    Deletes a file from the simulated filesystem (i.e., the SQLite database).
    :param filename: The name of the file to be deleted.
    """
    parent = 1

    if fsDB:
        # Check if the file exists in the database
        filters = {"name": filename, "parent_id": parent}  # Use a dictionary for filters
        file_record = fsDB.read_data("files", filters)
        
        if file_record:
            # Delete file record from the database
            fsDB.delete_data("files", "name", filename)
            return {"message": f"File '{filename}' deleted from the database."}
        else:
            raise HTTPException(status_code=404, detail="File not found in database.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.get("/file")
def read_file(filename: str):
    """
    Reads the contents of a file from the simulated filesystem and logs the read action in the database.
    :param filename: The name of the file to read.
    """
    parent = 13
    if fsDB:
        filters = {"name": filename, "parent_id": parent}  # Use a dictionary for filters
        file_record = fsDB.read_data("files", filters)
        if file_record:
            content = file_record.get("content")  # Assuming you store content in the DB
            fsDB.insert_action(filename, "read")  # Log the read action
            return {"content": content}
        else:
            raise HTTPException(status_code=404, detail="File not found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.post("/filePath")
def write_file(filename: str, content: str):
    """
    Write data to a file in the simulated filesystem and log the write operation in the database.
    :param filename: The name of the file to write to.
    :param content: The content to write to the file.
    """
    if fsDB:
        file_record = fsDB.read_data("files", filename)
        if file_record:
            fsDB.update_file(filename, {"content": content, "modified_at": CURRENT_TIMESTAMP})
            fsDB.insert_action(filename, "written")  # Log the write action
            return {"message": f"Content written to {filename}."}
        else:
            raise HTTPException(status_code=404, detail="File not found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.put("/mv")
def rename_file(old_filename: str, new_filename: str):
    """
    Rename a file in the simulated filesystem and update the database with the new name.
    :param old_filename: The current file name.
    :param new_filename: The new file name.
    """
    if fsDB:
        file_record = fsDB.read_data("files", old_filename)
        if file_record:
            fsDB.update_filename(old_filename, new_filename)
            return {"message": f"File renamed from {old_filename} to {new_filename}."}
        else:
            raise HTTPException(status_code=404, detail="File not found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.post("/dir")
def create_directory(directory_name: str):
    """
    Create a new directory in the simulated filesystem and log the action in the database.
    """
    if fsDB:
        existing_dir = fsDB.read_data("directories", directory_name)
        if existing_dir:
            raise HTTPException(status_code=400, detail="Directory already exists.")
        
        parent_id = 1  # Assuming root directory; change if necessary
        fsDB.insert_data(
            "directories", (None, directory_name, parent_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        )
        return {"message": f"Directory '{directory_name}' created successfully."}
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


@app.delete("/dir")
def delete_directory(directory_name: str):
    """
    Delete a directory and its contents from the simulated filesystem (database) and log the action.
    """
    if fsDB:
        directory_record = fsDB.read_data("directories", directory_name)
        if directory_record:
            fsDB.delete_data("directories", "name", directory_name)
            return {"message": f"Directory '{directory_name}' deleted from the database."}
        else:
            raise HTTPException(status_code=404, detail="Directory not found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)
