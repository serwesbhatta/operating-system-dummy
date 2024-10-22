from texttable import Texttable
from database.sqliteCRUD import SqliteCRUD
from .get_flags import get_flags

fsDB = SqliteCRUD("../database/data/filesystem.db")

def human_readable_size(size):
    """Convert size in bytes to a human-readable format."""
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if size < 1024:
            return f"{size:.1f}{unit}B"
        size /= 1024
    return f"{size:.1f}PB"  # In case size is very large

def format_permissions(user_permissions, world_permissions, is_directory=False):
    """Convert permission numbers into rwx format for user/group/others."""
    permission_str = 'd' if is_directory else '-'

    permission_str += 'r' if user_permissions[0] == 1 else '-'
    permission_str += 'w' if user_permissions[1] == 1 else '-'
    permission_str += 'x' if user_permissions[2] == 1 else '-'

    permission_str += '---'

    permission_str += 'r' if world_permissions[0] == 1 else '-'
    permission_str += 'w' if world_permissions[1] == 1 else '-'
    permission_str += 'x' if world_permissions[2] == 1 else '-'
    
    return permission_str

def get_owner_name(fsDB, owner_id):
    """Fetch the username of the owner based on the owner_id from the 'users' table."""
    filters = {"user_id": owner_id}
    user_record = fsDB.read_data("users", filters)
    if user_record:
        return user_record[0][1]  # Assuming username is the second column in the 'users' table
    return "unknown"

def ls(params=None):
    """Simulates the ls command with flags -a, -l, and -h."""
    # Parse the parameters (flags)
    show_hidden = False
    long_format = False
    human_format = False

    flags = get_flags(params)
    
    if flags:
        if "a" in flags:
            show_hidden = True
        if "l" in flags:
            long_format = True
        if "h" in flags:
            human_format = True
    
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

    # Set a maximum width
    table.set_max_width(0)  # 0 allows for unlimited width
    
    # If long format, add headers for permissions, owner, size, and date
    if long_format:
        table.header(['Permissions', 'Owner', 'Owner ID', 'Size', 'Created', 'Modified', 'Name'])
    
    # Process directories first
    for directory in directories:
        dir_name = directory[3]
        dir_user_permissions = directory[6:9]
        dir_world_permissions = directory[9:12]
        dir_owner_id = directory[2]
        dir_owner_name = get_owner_name(fsDB, dir_owner_id)
        dir_created_at = directory[4]
        dir_modified_at = directory[5]

        # Skip hidden directories unless -a is provided
        if not show_hidden and dir_name.startswith('.'):
            continue

        if long_format:
            # Build the output for long listing (-l) format
            permissions_str = format_permissions(dir_user_permissions, dir_world_permissions,is_directory=True)
            table.add_row([permissions_str, dir_owner_name, dir_owner_id, 0, dir_created_at, dir_modified_at, f"{dir_name}/"])
        else:
            table.add_row([f"{dir_name}/"])

    # Process files
    for file_entry in files:
        file_name = file_entry[3]
        file_size = file_entry[4]
        file_user_permissions = file_entry[8:11]
        file_world_permissions = file_entry[11:14]
        file_owner_id = file_entry[2]
        file_owner_name = get_owner_name(fsDB, file_owner_id)
        file_created_at = file_entry[5]
        file_modified_at = file_entry[6]

        # Skip hidden files unless -a is provided
        if not show_hidden and file_name.startswith('.'):
            continue

        if long_format:
            # Convert size to human-readable format if -h is provided
            if human_format:
                file_size = human_readable_size(file_size)

            # Build the output for long listing (-l) format
            permissions_str = format_permissions(file_user_permissions, file_world_permissions)
            table.add_row([permissions_str, file_owner_name, file_owner_id, file_size, file_created_at, file_modified_at, file_name])
        else:
            table.add_row([file_name])

    # Return the formatted table as a string
    return table.draw()
