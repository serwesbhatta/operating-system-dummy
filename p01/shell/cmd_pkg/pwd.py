# cmd_pkg/pwd.py
from .fs_state_manager import Fs_state_manager

def pwd():
    return Fs_state_manager.get_path()
