from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD

async def Get_files(fsDB: SqliteCRUD, pid: int, name : str =None):
    """
    Get a list of files from the simulated filesystem (from the database).
    """
    if name:
        filters = {"name": name, "pid": pid}
    else:
        filters = {"pid": pid}
    if fsDB:
        if name:
            try:
                files = fsDB.read_data("files", filters)
            except:
                raise HTTPException(status_code=404, detail="Could not read data")
        if files:
            return files
        else:
            raise HTTPException(status_code=404, detail="No files found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")