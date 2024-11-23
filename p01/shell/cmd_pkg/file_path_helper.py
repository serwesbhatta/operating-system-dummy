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

    if path_arr[0][0] == "/":
      pid = 1
    
    directories_exist = False
    file_exist = False
    
    if len(path_arr) > 0:
      for dir in path_arr:
        if dir == "..":
          try:
            response = call_api("parentDir", params={"id": pid})
          except:
            return {
            "directories_exist" : directories_exist,
            "file_exist": file_exist,
            "file_name": file_name,
            "pid": pid,
            "oid": oid,
          }
          if response:
            pid = response["pid"]
          
        else:
          filters = {"oid": oid, "pid": pid, "name": dir}
          
          try:
            response = call_api("dirs", params=filters)
            if response:
              pid = response[0]["id"]

          except:
            return {
            "directories_exist" : directories_exist,
            "file_exist": file_exist,
            "file_name": file_name,
            "pid": pid,
            "oid": oid,
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
        "file_name": file_name,
        "pid": pid,
        "oid": oid,
      }
  
  except Exception as e:
    print(f"Error in file_path_helper: {e}")
    return ""
