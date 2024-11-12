from cmd_pkg.pwd import pwd
from .whoami import whoami
from rich.console import Console
from rich.style import Style

console = Console()

def prompt():
  # Getting the current directory to show to the prompt
  current_directory = pwd()

  # Sliting the path by "/"
  path_parts = current_directory.split("/")

  # Get the last three folders
  current_directory ="/".join(path_parts[-3:])

  # Get current user
  user = whoami()

  # ANSI color codes
  GREEN = "\033[92m"  # Green color
  BLUE = "\033[94m"   # Blue color
  YELLOW = "\033[93m" # Yellow color
  RESET = "\033[0m"   # Reset color to default

  # Construct the prompt with colors
  prompt = f"{GREEN}({user}){RESET} {BLUE}{current_directory}{RESET} {YELLOW}$ {RESET}"

  return prompt