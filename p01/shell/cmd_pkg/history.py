from datetime import datetime
from cmd_pkg.fs_state_manager import Fs_state_manager
from .call_api import call_api

# Get current timestamp for logging or history entries
CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def history(cmd=None):
    """
    Retrieve or create a history file for each user based on their OID (owner ID).
    """
    try:
        # Retrieve owner ID for the current user and create a unique filename
        oid = Fs_state_manager.get_oid()
        filename = f"history_{oid}.txt"
        
        # Define the parameters to check if the file exists
        file_check_params = {"pid": 1, "filename": filename}
        
        # Attempt to fetch history file content via API
        existing_history = call_api("/file", "get", params=file_check_params)
        
        if existing_history == 404:  # File doesn't exist; create it
            create_file_params = {"pid": 1, "name": filename}
            create_response = call_api("/touch", "post", data=create_file_params)
            if create_response != 201:  # Assuming 201 is the success code for creation
                print(f"Failed to create history file for OID {oid}")
            else:
                print(f"New history file created for OID {oid}: {filename}")
        else:
            # Process existing history commands if file was found
            print(f"Existing history retrieved for OID {oid}: {existing_history}")
        
    except Exception as e:
        print(f"Error accessing history file: {e}")
    
    return ""  # Optional: return a status message or content

