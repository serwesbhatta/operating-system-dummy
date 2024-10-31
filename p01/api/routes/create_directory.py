from fastapi import HTTPException
from datetime import datetime
from database.sqliteCRUD import SqliteCRUD

def Create_directory(fsDB: SqliteCRUD, directory_name: str, parent_id: int, owner_id: int = None):
    """
    Create a new directory in the simulated filesystem and log the action in the database.
    :param directory_name: The name of the new directory.
    :param parent_id: The ID of the parent directory.
    :param owner_id: The ID of the owner (optional).
    """
    if fsDB:
        # Check if the directory already exists
        filters = {"name": directory_name, "pid": parent_id} 
        existing_dir = fsDB.read_data("directories", filters)
         
        if existing_dir:
            raise HTTPException(status_code=400, detail="Directory already exists.")
        
        # Insert the new directory into the database
        fsDB.insert_data(
            "directories", (None, parent_id, owner_id, directory_name, datetime.now(), datetime.now(),
            1, 0, 1, 1, 0, 1)  # Permissions and default values
        )
        
        return {"message": f"Directory '{directory_name}' created successfully."}
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")
