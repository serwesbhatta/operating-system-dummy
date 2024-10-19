from fastapi import HTTPException
from datetime import datetime

from database.sqliteCRUD import SqliteCRUD

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def Create_file(fsDB: SqliteCRUD, name: str):
    """
    Create a new file in the simulated filesystem and record the action in the database.
    """
    parent = 1
    if fsDB:
        parent = 1  # Assuming 1 is the root directory ID; update based on the schema
        filters = {'name': name, 'pid': parent}

        existing_file = fsDB.read_data("files", filters)

        print("Database is initialized")

        if existing_file:
            print("File already exists")
            raise HTTPException(status_code=400, detail="File already exists.")

        print("Inserting Data")

        # Insert values corresponding to the specified columns
        values = (
            None, parent, 1, name, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, None,
            1, 1, 1, 1, 0, 1  # Permissions and default values
        )

        fsDB.insert_data("files", values)
        
        return {"message": f"File '{name}' created successfully."}
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")
