from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from .get_column_names import Get_column_names
from .encoder_decoder import Decode

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
            rows = [dict(zip(column_names, row)) for row in files]
            for row in rows:
                print(row)
                if row["contents"] is not "NULL":
                    try:
                        row["contents"] = Decode(row["contents"])
                    except:
                        row["contents"] = "Cannot Decode"
            return rows
        else:
            raise HTTPException(status_code=404, detail="No files found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")