from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD

def Delete_file(fsDB: SqliteCRUD, pid: int, filename: str):
    """
    Deletes a file from the simulated filesystem (i.e., the SQLite database).
    :param filename: The name of the file to be deleted.
    """
    if fsDB:
        # Check if the file exists in the database
        filters = {"name": filename, "pid": pid}  # Use a dictionary for filters
        file_record = fsDB.read_data("files", filters)
        
        if file_record:
            # Delete file record from the database
            fsDB.delete_data("files", "name", filename)
            return {"message": f"File '{filename}' deleted from the database."}
        else:
            raise HTTPException(status_code=404, detail="File not found in database.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")