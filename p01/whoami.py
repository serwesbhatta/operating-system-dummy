import getpass

def whoami():
  current_user = getpass.getuser()
  return current_user
  