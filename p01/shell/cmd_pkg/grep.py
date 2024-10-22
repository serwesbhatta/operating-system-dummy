import re
from .get_flags import get_flags
from api.routes import Read_file
from .fs_state_manager import Fs_state_manager
from database.sqliteCRUD import SqliteCRUD

# Ensure fsDB is initialized (you might need to adjust the path)
fsDB = SqliteCRUD("../database/data/filesystem.db")

def grep(params):
    # Initial setup for flags
    flags = get_flags(params)
    case_insensitive = 'i' in flags
    count_matches = 'c' in flags
    list_filenames = 'l' in flags

    # Identify where the pattern and filenames start
    pattern_index = next((i for i, item in enumerate(params) if not item.startswith('-')), None)
    if pattern_index is None:
        return "Error: No pattern provided."

    pattern = params[pattern_index]
    files = params[pattern_index + 1:]  # Everything after the pattern is considered a filename

    if not files:
        return "Error: No files provided."

    results = []

    for filename in files:
        try:
            # Get current directory's pid and user ID
            oid = Fs_state_manager.get_oid()

            # Fetch file content using Read_file function
            file_content = Read_file(fsDB, filename, oid)  # Pass fsDB, filename, and user_id
            if file_content:
                lines = file_content.split('\n')
                matches = [line for line in lines if re.search(pattern, line, re.IGNORECASE if case_insensitive else 0)]

                if matches:
                    if list_filenames:
                        results.append(filename)
                    elif count_matches:
                        results.append(f"{filename}: {len(matches)}")
                    else:
                        results.extend(f"{filename}: {line}" for line in matches)
        except Exception as e:
            # Handle exceptions such as HTTPExceptions from failed API calls
            results.append(f"Error reading file {filename}: {str(e)}")

    return '\n'.join(results)
