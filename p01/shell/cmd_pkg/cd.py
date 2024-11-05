from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
from .getch import Getch
from .cat import cat

fsDB = SqliteCRUD("../database/data/filesystem.db")

getch = Getch() 

def cd(params=None):
    # from shell import ppointer

    # If params is None, treat it as an empty list
    if params is None:
        params = []

    current_pid = Fs_state_manager.get_pid()

    # Determine the new directory based on input parameters
    if len(params) == 0:
        print(f"\nNo directory specified. Current path: {Fs_state_manager.get_path()}")
        return ""  # Do nothing and keep the path unchanged

    current_path = Fs_state_manager.get_path()
    current_path = current_path.split("/")

    path = params[0].split("/")

    if params[0][0] == "/":
        current_path = ["~"]
        current_pid = 1
        path.pop(0)

    for dir in path:
        if dir == "~":
            Fs_state_manager.set_path(["~"])
            Fs_state_manager.set_pid(1)
            current_pid = 1
        
        else:
          if dir == "..":
            if current_pid > 1:
                parent_info = fsDB.get_parent_directory(current_pid)
                if parent_info:
                    dir = parent_info['name']
                    current_pid = parent_info['pid']
                    current_path.pop()  # Remove last directory in the path
                else:
                    current_path = ["~"]
                    current_pid = 1
            else:
                print("\nCan't go beyond root directory.")
                return ""

          elif fsDB.directory_exists(dir, current_pid):
              current_path.append(dir)
              current_pid = fsDB.get_directory_pid(dir, current_pid)
          else:
              print_path = "/".join(current_path)
              print(f"\nError: Directory '{dir}' does not exist in the path '{print_path}'.")
              return ""
    
    Fs_state_manager.set_pid(current_pid)
    Fs_state_manager.set_path(current_path)
    return ""

