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
async def get_files(name=None):
    """
    Get a list of files from the simulated filesystem (from the database).
    """
    if name:
        filters = {"name": name}
    if fsDB:
        if name:
            files = fsDB.read_data("files", filters)
        else:
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
    Create a new file in the simulated filesystem and record the action in the database.
    """
    parent = 1
    if fsDB:
        parent = 1  # Assuming 1 is the root directory ID; update based on the schema
        filters = {'name': name, 'pid': parent}

        existing_file = fsDB.read_data("files", filters)

        print("Database is initialized")

        if existing_file:
            print("File already exists")
            raise HTTPException(status_code=400, detail="File already exists.")

        print("Inserting Data")

        # Insert values corresponding to the specified columns
        values = (
            None, parent, None, name, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, None,
            1, 0, 1, 1, 0, 1  # Permissions and default values
        )

        fsDB.insert_data("files", values)
        
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
        filters = {"name": filename, "pid": parent}  # Use a dictionary for filters
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
def read_file(filename: str, user_id: int):
    """
    Reads the contents of a file from the simulated filesystem and logs the read action in the database.
    :param filename: The name of the file to read.
    :param user_id: The ID of the user trying to read the file.
    """
    if fsDB:
        response = fsDB.get_file_content(filename, user_id)
        if response["success"]:
            return response["content"]
        else:
            raise HTTPException(status_code=response["status"], detail=response["message"])
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
