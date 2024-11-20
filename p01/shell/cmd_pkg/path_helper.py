from .call_api import call_api
from .fs_state_manager import Fs_state_manager

def path_helper(path: str):
    """
    General-purpose function to resolve a given path and return metadata.

    Args:
        path (str): The input path (e.g., "data/earthquake/new_data.txt").
    
    Returns:
        dict: {
            "success": bool, 
            "message": str, 
            "pid": int or None,       # Parent directory ID
            "file_id": int or None,  # File ID if it exists and is a file
            "is_file": bool          # True if path points to a file
        }
    """
    # Split the path into components
    path_array = path.split("/")
    
    # Fetch initial OID and PID
    oid = Fs_state_manager.get_oid()
    pid = Fs_state_manager.get_pid()  # Start from the root directory
    
    current_pid = pid
    file_id = None
    is_file = False
    path_exists = True
    message = "Path resolved successfully."

    # Traverse the path components
    for i, individual_path in enumerate(path_array):
        # Check if it's the last component
        is_last_component = (i == len(path_array) - 1)
        
        # Check for directories in the current PID
        dir_params = {"oid": oid, "pid": current_pid, "name": individual_path}
        dir_response = call_api("dirs", "get", params=dir_params)
        
        if dir_response and "id" in dir_response:
            # Update current_pid if it's a directory
            current_pid = dir_response["id"]
        else:
            # Check if it's a file (only for the last component)
            if is_last_component:
                file_params = {"oid": oid, "pid": current_pid, "name": individual_path}
                file_response = call_api("files", "get", params=file_params)
                if file_response and "id" in file_response:
                    file_id = file_response["id"]
                    is_file = True
                else:
                    path_exists = False
                    break
            else:
                # Invalid path if it's not the last component and not a directory
                path_exists = False
                break

    # Return final response
    return {
        "success": path_exists,
        "message": message if path_exists else "Invalid path.",
        "pid": current_pid if path_exists else None,
        "file_id": file_id if path_exists else None,
        "is_file": is_file
    }
