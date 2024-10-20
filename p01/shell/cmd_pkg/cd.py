import os
from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager  # Update with the actual module name where fs_state_manager is defined

# Assuming fsDB is a global instance of SqliteCRUD
fsDB = SqliteCRUD("../database/data/filesystem.db")  # Adjust the path as needed

def cd(params):
    """Change the current directory.

    Args:
        params (list): A list of arguments passed to the command.
                        The first argument is the target directory.

    If no argument is provided, it changes the directory to the root.
    """
    # Access the global ppointer from shell.py
    from shell import ppointer

    # Determine the target directory
    if len(params) == 0:
        # If no argument is provided, default to root directory
        new_dir = "/"
    elif params[0] == "..":
        # Go to the parent directory
        if len(Fs_state_manager.current_path) > 1:
            Fs_state_manager.current_path.pop()  # Remove the last directory
        else:
            # Stay at root
            Fs_state_manager.current_path = ["~"]
        new_dir = Fs_state_manager.get_path()
    else:
        new_dir = params[0]

    # Construct the absolute path based on the current path
    if new_dir.startswith("/"):
        # Absolute path provided
        target_path = new_dir
    else:
        # Relative path provided
        target_path = os.path.join(Fs_state_manager.get_path(), new_dir)

    # Check if the target directory exists in the database
    if fsDB.directory_exists(new_dir):  # You may need to implement this method
        # Update the current path and directory
        Fs_state_manager.set_path(Fs_state_manager.current_path + [new_dir])  # Append new directory
        ppointer["current_path"] = target_path
        ppointer["current_dir"] = new_dir
        print(f"\nChanged directory to: {target_path}\n")  # Print on a new line
    else:
        print(f"\nError: Directory '{new_dir}' does not exist.\n")  # Print on a new line

    return ""
