import os
from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager

fsDB = SqliteCRUD("../database/data/filesystem.db")

def cd(params):
    from shell import ppointer

    current_pid = Fs_state_manager.get_pid()

    if len(params) == 0:
        new_dir = "~"
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
        new_dir = params[0]

    # Handle the root directory change
    if new_dir == "~":
        Fs_state_manager.set_path(["~"])
        Fs_state_manager.set_pid(1)
    elif fsDB.directory_exists(new_dir, current_pid):
        # If the directory exists and is not the current path
        current_path = Fs_state_manager.get_path().split("/")
        if new_dir not in current_path:
            Fs_state_manager.set_path(Fs_state_manager.current_path + [new_dir])
            new_pid = fsDB.get_directory_pid(new_dir, current_pid)
            Fs_state_manager.set_pid(new_pid)
        else:
            print(f"\nWarning: You are already in the directory '{new_dir}'.\n")
            return ""
    elif fsDB.file_belongs_to_directory(new_dir, current_pid):
        # If the specified path is a file in the current directory
        print(f"\n'{new_dir}' is a file. Would you like to open it? (Yes/No)\n")
        # You can add logic here to open the file or show its contents if needed
        return ""
    else:
        # Error message only if it's not a parent directory move
        if params[0] != "..":
            print(f"\nError: '{new_dir}' does not exist or is not accessible from the current directory '{Fs_state_manager.get_path()}'.\n")
            return ""

    ppointer["current_path"] = Fs_state_manager.get_path()
    ppointer["current_dir"] = new_dir
    print(f"\nChanged directory to: {Fs_state_manager.get_path()}")
    return ""