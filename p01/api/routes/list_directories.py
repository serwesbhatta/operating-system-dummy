from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD

def List_directories(fsDB: SqliteCRUD, oid: int, pid: int):
    """
    List all directories under a specific parent directory in the simulated filesystem.
    :param pid: The ID of the parent directory (default is root directory with ID 1).
    """
    if fsDB:
        # Fetch directories under the specified parent directory
        filters = {"oid": oid, "pid": pid}  # pid represents parent directory ID
        directories = fsDB.read_data("directories", filters)
        
        if directories:
            return {"directories": directories}
        else:
            raise HTTPException(status_code=404, detail="No directories found under the specified parent directory.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")