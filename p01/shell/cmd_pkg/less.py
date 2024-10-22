from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
fsDB = SqliteCRUD("../database/data/filesystem.db")



def less(params):
    """Display file content with navigation (forward and backward)."""
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
            PAGE_SIZE = 38  # Number of lines per page

            index = 0  # Start at the beginning of the file
            while True:
                # Clear the screen (or simulate clearing with new lines)
                print("\n"*1 )
                
                # Print the current page
                print("\n".join(lines[index:index + PAGE_SIZE]))

                # Get user input for navigation
                user_input = input('--Less-- (Press Enter to scroll forward, b to scroll back, q to quit): ')

                if user_input.lower() == 'q':
                    break
                elif user_input == '':  # Enter to scroll forward
                    index = min(index + PAGE_SIZE, len(lines))
                    if index >= len(lines):
                        print("--End of File--")
                        break
                elif user_input == 'b':  # 'b' to scroll back
                    index = max(index - PAGE_SIZE, 0)
                else:
                    print("\nInvalid input. Press Enter to continue or 'q' to quit.\n")

        else:
            print(f"\nError: Could not read the contents of '{file_name}'.\n")
    else:
        print(f"\nError: File '{file_name}' does not exist in the current directory.\n")

    return ""
