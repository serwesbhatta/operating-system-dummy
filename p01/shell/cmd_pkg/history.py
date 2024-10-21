# cmd_pkg/pwd.py

import os
from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
from datetime import datetime

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fsDB = SqliteCRUD("../database/data/filesystem.db")


def history(cmd = None):
    file_name = "history.txt"
    result = []
    result_string = ""
    values = (
            None, 1, 1, file_name, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, None,
            1, 1, 1, 1, 0, 1  # Permissions and default values
        )
    if not fsDB.file_belongs_to_directory(file_name, 1):
        fsDB.insert_data("files",values)
    if cmd!= None:
        filters = {"name": "history.txt", "pid": 1}
        file_record = fsDB.read_data("files", filters)
        file_id = file_record[0][0]
        # print(file_record)
        if file_record[0][7]!= None:
            count = len(file_record[0][7].split("\n"))
            new_contents = file_record[0][7] + "\n" + str(count) + " " + cmd
        else:
            new_contents = "0 " + cmd
        # new_contents = None
        fsDB.update_data("files", "contents", new_contents, "id", file_id)  
        return ""
    else:
        filters = {"name": "history.txt", "pid": 1}
        file_record = fsDB.read_data("files", filters)
        result = file_record[0][7].split("\n")
        for i in result:
            result_string += i+"\n"
    
    return result_string
