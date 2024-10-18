from fastapi import HTTPException
from datetime import datetime

from database.sqliteCRUD import SqliteCRUD

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def Create_directory(fsDB: SqliteCRUD, directory_name: str):
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