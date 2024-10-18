from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD

async def Get_files(fsDB: SqliteCRUD, name=None):
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