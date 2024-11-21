from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
from datetime import datetime
from .file_path_helper import file_path_helper
from .call_api import call_api
import json
CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


fsDB = SqliteCRUD("../database/data/filesystem.db")

def touch(params = None):
    """Create a new file or update the timestamp of an existing file."""
    if not params:
        print("\nPlease specify the filename or the filepath")
        return ""

    file_path = params[0]
    file_path_arr = file_path.split("/")

    if len(file_path_arr) > 1:
        response = file_path_helper(file_path)

        if response["directories_exist"] and response["file_exist"]:
            print("\nFile already exist")
        elif response["directories_exist"]:
            oid = response["oid"]
            pid = response["pid"]
            file_name = file_path_arr[-1]
            new_file_filters = {"oid": oid, "pid": pid, "name": file_name}
            new_file_response = call_api("touch", "post", data=new_file_filters)
            if new_file_response:
                message = new_file_response["message"]
                print(f"\n{message}")
            else:
                print("\nCannot create the file")
        else:
            print("\nDirectory not found")
    
    else:
        pid = Fs_state_manager.get_pid()
        oid = Fs_state_manager.get_oid()
        file_name = file_path

        filters = {"oid": oid, "pid": pid, "name": file_name}

        new_file_response = call_api("touch", "post", data=filters)

        if new_file_response:
            message = new_file_response["message"]
            print(f"\n{message}")
        else:
            print("Cannot create the file")
    return ""
