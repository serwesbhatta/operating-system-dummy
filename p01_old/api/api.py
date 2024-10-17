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
def write_file(filepath: str, content: str, user_id: int):
    """
    Writes data to a file and logs the write operation in the database.
    :param filepath: The path of the file to write to.
    :param content: The content to write to the file.
    :param user_id: The ID of the user attempting to write to the file.
    """
    parent = 1  # Assuming the root directory for simplicity. This can be dynamic.
    if fsDB:
        # Check if the file exists and fetch it
        filters = {"name": filepath, "pid": parent}
        file_record = fsDB.read_data("files", filters)
        
        if file_record:
            file_id = file_record[0][0]  # File ID
            owner_id = file_record[0][2]  # Owner ID
            write_permission = file_record[0][9]  # Write permission
            world_write = file_record[0][12]  # World write permission

            # Check if the user has permission to write
            if (user_id == owner_id and write_permission == 1) or world_write == 1:
                # Use the generic update_data function to update the contents
                update_status = fsDB.update_data("files", "contents", content, "id", file_id)
                if update_status["success"]:
                    return {"message": f"Content written to file '{filepath}' successfully."}
                else:
                    raise HTTPException(status_code=500, detail=update_status["message"])
            else:
                raise HTTPException(status_code=403, detail="Permission denied to write to the file.")
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
