from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
fsDB = SqliteCRUD("../database/data/filesystem.db")


def head(params):
    """Display the first N lines of a file."""
    if len(params) < 1:
        print("\nError: No file specified.\n")
        return

    file_name = params[0]
    num_lines = 10  # Default to 10 if no -n option is provided

    # Check if -n option is provided
    if len(params) == 3 and params[1] == '-n':
        try:
            num_lines = int(params[2])
            if num_lines < 1:
                print("\nError: Number of lines must be a positive integer.\n")
                return
        except ValueError:
            print("\nError: Invalid number of lines specified. It must be an integer.\n")
            return
    elif len(params) > 1 and params[1] != '-n':
        print("\nError: Invalid command format. Use -n followed by a number.\n")
        return

    current_pid = Fs_state_manager.get_pid()

    # Fetch file contents from the database
    if fsDB.file_exists(file_name, current_pid):
        file_contents = fsDB.get_file_contents(file_name, current_pid)
        
        if file_contents is not None:
            # Handle binary files
            if isinstance(file_contents, bytes):
                try:
                    file_contents = file_contents.decode('utf-8')
                except UnicodeDecodeError:
                    print(f"\nError: File '{file_name}' contains binary data and cannot be displayed as text.\n")
                    return

            # Split file contents into lines
            lines = file_contents.split('\n')
            # Print the first num_lines
            print("\n")
            print("\n".join(lines[:num_lines]))

        else:
            print(f"\nError: Could not read the contents of '{file_name}'.\n")
    else:
        print(f"\nError: File '{file_name}' does not exist in the current directory.\n")

    return ""

