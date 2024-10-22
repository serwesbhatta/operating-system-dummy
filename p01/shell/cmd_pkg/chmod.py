from .get_flags import get_flags
from api.routes.set_file_permissions import Set_file_permissions
from .fs_state_manager import Fs_state_manager
from database.sqliteCRUD import SqliteCRUD
from .cd import cd

# Ensure fsDB is initialized (you might need to adjust the path)
fsDB = SqliteCRUD("../database/data/filesystem.db")

def chmod(params):
  # Split the params_str to extract mode and path
  print()
  print(type(params))
  print(params)

  if not params:
      return False
  
  mode = params[0]
  full_path = ' '.join(params[1:])  # Join the remaining parts to form the path

  try:
    path, file_name = full_path.rsplit('/', 1)  # Split the path on the last occurrence of '/'
  except ValueError:
      path = ''  # Default to empty if no '/' found
      file_name = full_path  # The full path is the file name

  last_directory = path.split('/')[-1]
  path = [path]
  print(path)
  cd(path)

  if Fs_state_manager.current_directory == last_directory:
    message = Set_file_permissions(fsDB, mode, path)
    if message == True:
       print("File permission changed successfully")
    else:
       print("Error. Cannot change the permissions")
  else:
     print("Path is not available so cannot do chmod")

  print(f"This is the full_path: {full_path}")
  print(f"This is the path {path}")
  print(f"This is the flename {file_name}")

  # if not path or not mode:
  #     return "Error: Missing path or mode argument."

  # try:
  #     # Convert mode from string in octal format to an integer
  #     mode = int(mode, 8)
  # except ValueError:
  #     return "Error: Invalid mode. Please use a valid octal number."
  
  # # Get file or directory ID based on path
  # file_id = fsDB.get_file_id_by_path(path)
  # if file_id is None:
  #     return f"Error: No file found at {path}."

  # # Update permissions in the database
  # success = fsDB.update_permissions(file_id, mode)
  # if success:
  #     return "Permissions changed successfully."
  # else:
  #     return "Failed to change permissions."