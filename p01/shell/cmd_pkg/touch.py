from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
from datetime import datetime
CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


fsDB = SqliteCRUD("../database/data/filesystem.db")

def touch(params):
    """Create a new file or update the timestamp of an existing file."""
    if len(params) == 0:
        print("\nError: No file name specified.")
        return

    file_name = params[0]
    current_pid = Fs_state_manager.get_pid()

    # Check if the file already exists in the current directory
    filters = {"name": file_name, "pid": current_pid}
    existing_file = fsDB.read_data("files", filters)

    if existing_file:
        # Update the modified_date timestamp of the existing file
        fsDB.update_data("files", "modified_date", CURRENT_TIMESTAMP, "name", file_name)
    else:
        # Insert a new file into the database
        fsDB.insert_data(
            "files", (None, current_pid, None, file_name, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
            None, 1, 0, 1, 1, 0, 1)  # Add any default values as needed
        )
        print(f"File '{file_name}' created successfully.")
    return ""  # Return an empty string to avoid printing None
