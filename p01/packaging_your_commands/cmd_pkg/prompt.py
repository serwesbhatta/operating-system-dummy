from .pwd import pwd
from .whoami import whoami

def prompt():
  # Getting the current directory to show to the prompt
  current_directory = pwd()

  # Sliting the path by "/"
  path_parts = current_directory.split("/")

  # Get the last three folders
  current_directory ="/".join(path_parts[-3:])

  # Get current user
  user = whoami()

  # Set the prompt string
  prompt = f"({user}) {current_directory} $"  # set default prompt

  return prompt