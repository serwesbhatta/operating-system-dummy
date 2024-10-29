from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from .get_column_names import Get_column_names

async def Get_files(fsDB: SqliteCRUD, pid: int, name : str =None):
    """
    Get a list of files from the simulated filesystem (from the database).
    """
    if name is not None:
        filters = {"name": name, "pid": pid}
    elif pid:
        filters = {"pid": pid}
    else:
        print("Please use the pid")
    
    if fsDB:
        try:
            files = fsDB.read_data("files", filters)
        except:
            raise HTTPException(status_code=404, detail="Could not read data")
        if files:
            column_names = await Get_column_names(fsDB, "files")
            return [dict(zip(column_names, row)) for row in files]
        else:
            raise HTTPException(status_code=404, detail="No files found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")