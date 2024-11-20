from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
from datetime import datetime
from .file_path_helper import file_path_helper
from .call_api import call_api
import json
CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


fsDB = SqliteCRUD("../database/data/filesystem.db")

def touch(params):
    """Create a new file or update the timestamp of an existing file."""
    if len(params) == 0:
        print("\nError: No file name specified.")
        return

    file_path = params[0]
    file_path_arr = file_path.split("/")

    if len(file_path_arr) > 1:
        # path_response = file_path_helper(file_name)
        # if path_response["success"] == True and path_response["is_file"] == True:
        #     file_name = file_path[-1]
        #     current_pid = path_response["pid"]
        # else:
        #     print("Path is not successful")
        #     return
        response = file_path_helper(file_name)

        with open("testfile2.json","w") as f:
            json.dump(response,f)

        if response["directories_exist"] and response["file_exist"]:
            print("File already exist")
        elif response["directories_exist"]:
            oid = response[0]["oid"]
            pid = response[0]["pid"]
            file_name = file_path_arr[-1]
            new_file_filters = {"oid": oid, "pid": pid, "name": file_name}
            with open("testfile.json","w") as f:
                json.dump(new_file_filters,f)
            new_file_response = call_api("touch", "post", data=new_file_filters)
            if new_file_response:
                print(new_file_response["message"])
            else:
                print("Cannot create the file")
        else:
            print("Directory not found")
    
    else:
        pid = Fs_state_manager.get_pid()
        oid = Fs_state_manager.get_oid()
        file_name = file_path

        filters = {"oid": oid, "pid": pid, "name": file_name}

        new_file_response = call_api("touch", "post", data=filters)

        if new_file_response:
            print(new_file_response["message"])
        else:
                print("Cannot create the file")
    return

    # current_pid = Fs_state_manager.get_pid()

    # # Check if the file already exists in the current directory
    # filters = {"name": file_name, "pid": current_pid}
    # existing_file = fsDB.read_data("files", filters)

    # if existing_file:
    #     # Update the modified_date timestamp of the existing file
    #     fsDB.update_data("files", "modified_date", CURRENT_TIMESTAMP, "name", file_name)
    # else:
    #     # Insert a new file into the database
    #     fsDB.insert_data(
    #         "files", (None, current_pid, None, file_name, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    #         None, 1, 0, 1, 1, 0, 1)  # Add any default values as needed
    #     )
    #     print(f"File '{file_name}' created successfully.")
    # return ""  # Return an empty string to avoid printing None
