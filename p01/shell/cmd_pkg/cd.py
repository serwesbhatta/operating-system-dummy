import os
from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager

fsDB = SqliteCRUD("../database/data/filesystem.db")

def cd(params=None):
    from shell import ppointer

    # If params is None, treat it as an empty list
    if params is None:
        params = []

    current_pid = Fs_state_manager.get_pid()

    # Determine the new directory based on input parameters
    if len(params) == 0:
        print(f"\nNo directory specified. Current path: {Fs_state_manager.get_path()}")
        return ""  # Do nothing and keep the path unchanged

    new_dir = params[0]

    # Handle the root directory change
    if new_dir == "~":
        Fs_state_manager.set_path(["~"])
        Fs_state_manager.set_pid(1)
    elif new_dir.startswith("/"):  # Absolute path
        # Split the absolute path into parts and check each part
        path_parts = new_dir.strip("/").split("/")
        new_path = []
        temp_pid = 1  # Start at the root PID

        for part in path_parts:
            if fsDB.directory_exists(part, temp_pid):
                new_path.append(part)
                temp_pid = fsDB.get_directory_pid(part, temp_pid)
            else:
                print(f"\nError: Directory '{part}' does not exist in the path '{new_dir}'.\n")
                return ""

        # Set the new path and PID
        Fs_state_manager.set_path(new_path)
        Fs_state_manager.set_pid(temp_pid)
        
    elif params[0] == "..":
        # Go to the parent directory
        if current_pid > 1:
            parent_info = fsDB.get_parent_directory(current_pid)
            if parent_info:
                new_dir = parent_info['name']
                Fs_state_manager.set_pid(parent_info['pid'])
                Fs_state_manager.current_path.pop()  # Remove last directory in the path
            else:
                new_dir = "~"
        else:
            new_dir = "~"  # Already at root, stay there
    else:
        # Relative path handling
        current_path = Fs_state_manager.get_path().split("/")
        if fsDB.directory_exists(new_dir, current_pid):
            # If the directory exists and is not the current path
            if new_dir not in current_path:
                Fs_state_manager.set_path(current_path + [new_dir])
                new_pid = fsDB.get_directory_pid(new_dir, current_pid)
                Fs_state_manager.set_pid(new_pid)
            else:
                print(f"\nWarning: You are already in the directory '{new_dir}'.\n")
                return ""
        elif fsDB.file_belongs_to_directory(new_dir, current_pid):
            # If the specified path is a file in the current directory
            print(f"\n'{new_dir}' is a file. Would you like to open it? (Yes/No)\n")
            return ""
        else:
            print(f"\nError: '{new_dir}' does not exist or is not accessible from the current directory '{Fs_state_manager.get_path()}'.\n")
            return ""

    ppointer["current_path"] = Fs_state_manager.get_path()
    ppointer["current_dir"] = new_dir
    print(f"\nChanged directory to: {Fs_state_manager.get_path()}")
    Fs_state_manager.current_directory = last_folder = ppointer["current_path"].split('/')[-1]
    return ""

