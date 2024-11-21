from .call_api import call_api
from .fs_state_manager import Fs_state_manager

def file_path_helper(path: str):
  """
  Helper function to validate file paths.

  :param path: The file path to validate.
  :return: Tuple (is_file, directory_id, filename) if valid, None otherwise.
  """
  try:
    path_arr = path.split("/")
    file_name = path_arr.pop()

    oid = Fs_state_manager.get_oid()
    pid = Fs_state_manager.get_pid()
    directories_exist = False
    file_exist = False

    for dir in path_arr:
      filters = {"oid": oid, "pid": pid, "name": dir}
      
      try:
        response = call_api("dirs", params=filters)
        if response:
          pid = response[0]["id"]

      except:
        return {
        "directories_exist" : directories_exist,
        "file_exist": file_exist,
        "pid": pid,
        "oid": oid,
        "id": id
      }
    
    directories_exist = True

    filters = {"oid": oid, "pid": pid, "name": file_name}
    
    try:
      response = call_api("files", filters)

      if response:
        file_exist = True

    except:
      pass
    
    return {
        "directories_exist" : directories_exist,
        "file_exist": file_exist,
        "pid": pid,
        "oid": oid,
        "id": id
      }
  
  except Exception as e:
    print(f"Error in file_path_helper: {e}")
    return ""
