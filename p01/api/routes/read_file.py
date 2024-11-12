from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from .encoder_decoder import Decode

def Read_file(fsDB: SqliteCRUD, oid:int, pid: int, filename: str):
    """
    Reads the contents of a file from the simulated filesystem and logs the read action in the database.
    :param filename: The name of the file to read.
    :param user_id: The ID of the user trying to read the file.
    """
    filters = {"oid" : oid, "name": filename, "pid": pid}
    if fsDB:
        response = fsDB.get_file_content(filters)
        if response["success"]:
            content = Decode(response["content"])  # No need to decode, assuming it's already a string
            return content
        else:
            raise HTTPException(status_code=response["status"], detail=response["message"])
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")
