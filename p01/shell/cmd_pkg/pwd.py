# cmd_pkg/pwd.py
from cmd_pkg.cwd_manager import cwd_manager

def pwd():
    return cwd_manager.get_path()
