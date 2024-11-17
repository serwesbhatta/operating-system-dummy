from .call_api import call_api
from .fs_state_manager import Fs_state_manager

def path_helper(path: str):
  path_array = path.split("/")

  oid = Fs_state_manager.get_oid()
  pid = Fs_state_manager.get_pid()

  filters = {"oid": oid, "pid": pid}
  path_exists = False

  for individual_path in path_array:
    filters["name"] = individual_path
    response = call_api("", )
  