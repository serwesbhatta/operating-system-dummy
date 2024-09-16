import my_pwd
from whoami import whoami

def prompt():
  current_user = whoami()
  current_directory = my_pwd.get_current_directory()
  prompt_string = "(" + current_user + "): " + current_directory + "$"
  return prompt_string
  