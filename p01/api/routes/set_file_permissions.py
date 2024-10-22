from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from database.operations.set_file_permissions_db import Set_file_permissions_db

fsDB = SqliteCRUD("../database/data/filesystem.db")

def Set_file_permissions(fsDB: SqliteCRUD, mode: int, filepath: str, oid, pid):
  if fsDB:
    filters = {"name": filepath, "oid": oid, "pid": pid}
    
    Set_file_permissions(fsDB, "files", mode, filters)