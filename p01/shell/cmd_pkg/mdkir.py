from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager

fsDB = SqliteCRUD("../database/data/filesystem.db")

def mkdir(params):
    """Create a new directory."""
    if len(params) == 0:
        print("\nError: No directory name specified.\n")
        return

    new_dir_name = params[0]
    current_pid = Fs_state_manager.get_pid()

    # Check if the directory already exists
    if fsDB.directory_exists(new_dir_name, current_pid):
        print(f"\nError: Directory '{new_dir_name}' already exists in the current directory.\n")
        return

    # Insert the new directory into the database
    # Assuming 'directories' table has columns like 'name', 'pid', and possibly others like 'oid' or 'created_at'
    fsDB.insert_data('directories', (new_dir_name, current_pid))  # Adjust this according to your schema

    print(f"\nDirectory '{new_dir_name}' created successfully.\n")
