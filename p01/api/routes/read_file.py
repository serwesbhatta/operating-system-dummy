from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from .base64isCrazy import decodeIt

def Read_file(fsDB: SqliteCRUD, filename: str, user_id: int):
    """
    Reads the contents of a file from the simulated filesystem and logs the read action in the database.
    :param filename: The name of the file to read.
    :param user_id: The ID of the user trying to read the file.
    """
    if fsDB:
        response = fsDB.get_file_content(filename, user_id)
        if response["success"]:
            content = response["content"]
            content = decodeIt(content)
            return content
        else:
            raise HTTPException(status_code=response["status"], detail=response["message"])
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")