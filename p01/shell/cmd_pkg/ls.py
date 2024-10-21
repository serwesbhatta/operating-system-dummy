from texttable import Texttable
from database.sqliteCRUD import SqliteCRUD

fsDB = SqliteCRUD("../database/data/filesystem.db")

def format_permissions(permission, is_directory=False):
    """Convert permission numbers into rwx format for user/group/others."""
    permission_str = 'd' if is_directory else '-'
    
    # For user permissions
    permission_str += 'r' if permission & 0b100000000 else '-'
    permission_str += 'w' if permission & 0b010000000 else '-'
    permission_str += 'x' if permission & 0b001000000 else '-'
    
    # Group permissions (we don't have them, so "---")
    permission_str += "---"
    
    # For others/world permissions
    permission_str += 'r' if permission & 0b000000100 else '-'
    permission_str += 'w' if permission & 0b000000010 else '-'
    permission_str += 'x' if permission & 0b000000001 else '-'
    
    return permission_str

def get_owner_name(fsDB, owner_id):
    """Fetch the username of the owner based on the owner_id from the 'users' table."""
    filters = {"user_id": owner_id}
    user_record = fsDB.read_data("users", filters)
    if user_record:
        return user_record[0][1]  # Assuming username is the second column in the 'users' table
    return "unknown"

def ls(fsDB: SqliteCRUD, params=None):
    """Simulates the ls command with flags -a, -l, and -h."""
    # Parse the parameters (flags)
    show_hidden = False
    long_format = False
    
    if params:
        if "-a" in params:
            show_hidden = True
        if "-l" in params:
            long_format = True
    
    # Fetch files and directories from the database
    current_directory_pid = 1  # This should be dynamic, fetched from the current path manager.
    
    # Fetch files from the 'files' table
    file_filters = {"pid": current_directory_pid}
    files = fsDB.read_data("files", file_filters)  # Assuming your file table uses 'pid' as the parent directory ID
    
    # Fetch directories from the 'directories' table
    dir_filters = {"pid": current_directory_pid}
    directories = fsDB.read_data("directories", dir_filters)  # Assuming your directories table has the same structure as files
    
    if not files and not directories:
        return "No files or directories found."

    # Prepare table output
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    
    # If long format, add headers for permissions, owner, size, and date
    if long_format:
        table.header(['Permissions', 'Owner', 'Owner ID', 'Size', 'Created', 'Modified', 'Name'])
    
    # Process directories first
    for directory in directories:
        dir_name = directory[3]  # Assuming 'name' is the 4th column
        dir_permissions = directory[6]  # Assuming 'permissions' are the 7th column
        dir_owner_id = directory[2]  # Assuming 'owner_id' is the 3rd column
        dir_owner_name = get_owner_name(fsDB, dir_owner_id)
        dir_created_at = directory[4]  # Assuming 'created_at' is the 5th column
        dir_modified_at = directory[5]  # Assuming 'modified_at' is the 6th column

        # Skip hidden directories unless -a is provided
        if not show_hidden and dir_name.startswith('.'):
            continue

        if long_format:
            # Build the output for long listing (-l) format
            permissions_str = format_permissions(dir_permissions, is_directory=True)
            table.add_row([permissions_str, dir_owner_name, dir_owner_id, 0, dir_created_at, dir_modified_at, f"{dir_name}/"])
        else:
            table.add_row([f"{dir_name}/"])

    # Process files
    for file_entry in files:
        file_name = file_entry[3]  # Assuming 'name' is the 4th column
        file_size = file_entry[4]  # Assuming 'size' is the 5th column
        file_permissions = file_entry[8]  # Assuming 'permissions' is the 9th column
        file_owner_id = file_entry[2]  # Assuming 'owner_id' is the 3rd column
        file_owner_name = get_owner_name(fsDB, file_owner_id)
        file_created_at = file_entry[6]  # Assuming 'created_at' is the 7th column
        file_modified_at = file_entry[7]  # Assuming 'modified_at' is the 8th column

        # Skip hidden files unless -a is provided
        if not show_hidden and file_name.startswith('.'):
            continue

        if long_format:
            # Build the output for long listing (-l) format
            permissions_str = format_permissions(file_permissions)
            table.add_row([permissions_str, file_owner_name, file_owner_id, file_size, file_created_at, file_modified_at, file_name])
        else:
            table.add_row([file_name])

    # Return the formatted table as a string
    return table.draw()
