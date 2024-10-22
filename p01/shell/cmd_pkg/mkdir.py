from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
from api.routes.create_directory import Create_directory

fsDB = SqliteCRUD("../database/data/filesystem.db")

def mkdir(params):
    """Create a new directory."""
    if len(params) == 0:
        print("\nError: No directory name specified.\n")
        return ""

    directory_name = params[0]
    current_pid = Fs_state_manager.get_pid()
    owner_id = None  # Set this to the appropriate owner ID if you have it

    # Check if the directory already exists in the current directory
    filters = {"name": directory_name, "pid": current_pid}
    existing_dir = fsDB.read_data("directories", filters)

    if existing_dir:
        print(f"\nError: Directory '{directory_name}' already exists in the current directory.")
        return ""

    # Attempt to create the directory
    try:
        Create_directory(fsDB, directory_name, current_pid, owner_id)
        print(f"Directory '{directory_name}' created successfully.")
        return ""
    except HTTPException as e:
        print(f"\nError: {e.detail}\n")
        return ""

