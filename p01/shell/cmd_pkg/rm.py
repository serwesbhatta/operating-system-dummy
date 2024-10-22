from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager

fsDB = SqliteCRUD("../database/data/filesystem.db")

def rm(params):
    """Remove a file from the current directory."""
    if len(params) == 0:
        print("Error: No file name specified.")
        return

    file_name = params[0]
    current_pid = Fs_state_manager.get_pid()
    filters = {"name": file_name, "pid": current_pid}
    existing_file = fsDB.read_data("files", filters)

    if existing_file:
        fsDB.delete_data("files", "name", file_name)  # Assuming name is unique per directory
        print(f"File '{file_name}' removed successfully.")
    else:
        print(f"Error: File '{file_name}' does not exist in the current directory.")

    return ""

