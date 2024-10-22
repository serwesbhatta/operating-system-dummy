
from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
fsDB = SqliteCRUD("../database/data/filesystem.db")



def more(params):
    """Display file content page by page."""
    if len(params) == 0:
        print("\nError: No file specified.\n")
        return

    file_name = params[0]
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
            PAGE_SIZE = 35  # Number of lines per page
            print("\n" )
            for i in range(0, len(lines), PAGE_SIZE):
                # Print a page worth of lines
                print("\n".join(lines[i:i + PAGE_SIZE]))

                # Wait for user input to show more
                user_input = input('--More-- (Press Enter to continue, q to quit): ')
                if user_input.lower() == 'q':
                    break
        else:
            print(f"\nError: Could not read the contents of '{file_name}'.\n")
    else:
        print(f"\nError: File '{file_name}' does not exist in the current directory.\n")

    return ""
