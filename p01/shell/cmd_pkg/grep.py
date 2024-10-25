import re
from .get_flags import get_flags
from api.routes import Read_file
from .fs_state_manager import Fs_state_manager
from database.sqliteCRUD import SqliteCRUD

# Ensure fsDB is initialized (you might need to adjust the path)
fsDB = SqliteCRUD("../database/data/filesystem.db")

def grep(params, input_data=None):
    if not params:
        return "Error: No parameters provided."

    # Initial setup for flags and separate filenames from flags
    flags = get_flags(params)
    case_insensitive = 'i' in flags
    count_matches = 'c' in flags
    list_filenames = 'l' in flags

    # Find the pattern and the files to process
    files = []
    pattern = None
    reading_files = False
    for index, item in enumerate(params):
        if item.startswith('-') and not reading_files:
            continue  # Skip flags before the pattern
        elif not pattern and not item.startswith('-'):
            pattern = item
            # Only take the next item as filename if it exists and is not a flag
            if index + 1 < len(params) and not params[index + 1].startswith('-'):
                files.append(params[index + 1])
            break  # Stop processing after finding the pattern and optional file

    if not pattern:
        return "Error: No pattern provided."
    if not files and not input_data:
        return "Error: No files provided or no input data."

    results = []

    # Function to search content
    def search_content(content, filename=""):
        lines = content.split('\n')
        matches = [line for line in lines if re.search(pattern, line, re.IGNORECASE if case_insensitive else 0)]

        if matches:
            if list_filenames:
                return [filename] if filename else []
            elif count_matches:
                return [f"{filename}: {len(matches)}"] if filename else [f"{len(matches)}"]
            else:
                return [f"{line}" for line in matches] if filename else matches
        return []

    # Process input data if provided
    if input_data:
        results.extend(search_content(input_data))
    else:
        for filename in files:
            try:
                file_content = Read_file(fsDB, filename, user_id=1)  # Assuming static user ID
                if file_content:
                    results.extend(search_content(file_content, filename))
            except Exception as e:
                results.append(f"Error reading file {filename}: {str(e)}")

    return '\n'.join(results)
