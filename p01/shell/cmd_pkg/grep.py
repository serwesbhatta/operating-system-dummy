import re
from .get_flags import get_flags
from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager

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
            # Get current directory's pid
            oid = Fs_state_manager.get_oid()

            # Fetch file content using API; ensure you handle errors or non-existence properly
            file_content = fsDB.(filename, oid)
            print(file_content)
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
