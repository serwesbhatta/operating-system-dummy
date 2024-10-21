from cmd_pkg.fs_state_manager import Fs_state_manager

def pwd(params=None):
    """Print the current working directory."""
    # Get the current path from the file system state manager
    current_path = Fs_state_manager.get_path()
    # print("\nCurrent dir\n",current_path,Fs_state_manager.__dict__)
    # Print the current path
    return current_path
