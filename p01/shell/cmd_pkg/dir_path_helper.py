from .call_api import call_api
from .fs_state_manager import Fs_state_manager

def dir_path_helper(path: str):
    """
    Helper function to validate and navigate directory paths.

    :param path: The directory path to validate.
    :return: Directory ID if valid, None otherwise.
    """
    try:
        path_array = path.split("/")
        oid = Fs_state_manager.get_oid()
        pid = Fs_state_manager.get_pid()
        filters = {"oid": oid, "pid": pid}
        current_dir_id = pid

        for dir_name in path_array:
            filters["name"] = dir_name
            response = call_api("directories", "get", params=filters)

            if response and response.get("data"):
                current_dir_id = response["data"][0]["id"]
                filters["pid"] = current_dir_id  # Update for next level
            else:
                print(f"Directory '{dir_name}' does not exist.")
                return None

        return current_dir_id
    except Exception as e:
        print(f"Error in dir_path_helper: {e}")
        return None
