from datetime import datetime
from database.sqliteCRUD import SqliteCRUD
from .get_files import Get_files

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def Move_file(fsDB: SqliteCRUD, oid: int, pid: int, name: str, target_pid: int):
    """
    Create a new file in the simulated filesystem and record the action in the database.
    """
    if fsDB:
        try:
            filters = {"oid": oid, "pid": pid, "name": name}

            try:
                response = Get_files(fsDB, oid, pid, name)

                if response["status"] == "fail":
                    return {"status": "fail", "message": "\nUnable to find the file."}
            except:
                return {"status": "fail", "message": "\nCannot get file from api."}

            new_values = {
                "pid": target_pid,
                "creation_date": CURRENT_TIMESTAMP,
                "modified_date": CURRENT_TIMESTAMP,
            }
            database_response = fsDB.update_multiple_data("files", filters, new_values)

            if database_response["success"]:
                return {
                    "status": "success",
                    "message": ""
                }

            else:
                return {
                    "status": "fail",
                    "message": f"\nCould not change the filepath.",
                }

        except:
            return {"status": "fail", "message": "\nCannot connect to database"}
    else:
        return {"status": "fail", "message": "\nDatabase not initialized."}
