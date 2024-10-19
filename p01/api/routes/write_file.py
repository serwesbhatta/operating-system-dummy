from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from .create_file import Create_file

def Write_file(fsDB: SqliteCRUD, filepath: str, content: str, user_id: int):
    """
    Writes data to a file and logs the write operation in the database.
    :param filepath: The path of the file to write to.
    :param content: The content to write to the file.
    :param user_id: The ID of the user attempting to write to the file.
    """
    parent = 1  # Assuming the root directory for simplicity. This can be dynamic.
    if fsDB:
        # Check if the file exists and fetch it
        filters = {"name": filepath, "pid": parent}
        file_record = fsDB.read_data("files", filters)
        
        if file_record:
            file_id = file_record[0][0]  # File ID
            owner_id = file_record[0][2]  # Owner ID
            write_permission = file_record[0][9]  # Write permission
            world_write = file_record[0][12]  # World write permission

            # Check if the user has permission to write
            if (user_id == owner_id and write_permission == 1) or world_write == 1:
                # Use the generic update_data function to update the contents
                update_status = fsDB.update_data("files", "contents", content, "id", file_id)
                if update_status["success"]:
                    return {"message": f"Content written to file '{filepath}' successfully."}
                else:
                    raise HTTPException(status_code=500, detail=update_status["message"])
            else:
                raise HTTPException(status_code=403, detail="Permission denied to write to the file.")
        else:
            Create_file(fsDB, filepath)
            Write_file(fsDB, filepath, content, user_id)
            return {"message": f"Created new file {filepath} sucessfully with the required content."}
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")