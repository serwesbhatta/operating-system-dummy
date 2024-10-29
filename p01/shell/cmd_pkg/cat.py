from database.sqliteCRUD import SqliteCRUD
from cmd_pkg.fs_state_manager import Fs_state_manager
from .call_api import call_api

fsDB = SqliteCRUD("../database/data/filesystem.db")

def cat(params):
    """Display the contents of one or more files."""
    if len(params) == 0:
        print("\nError: No file specified.\n")
        return

    filename = params[0]
    current_pid = Fs_state_manager.get_pid()
    filters = {"name": filename, "pid": current_pid}

    response = call_api("files", "get", params=filters)
        # url = f"http://localhost:8080/file?filename={fname}&user_id={1}"
        # response = requests.get(url)
    if response:
        content = response[0]["contents"]
        print(f"This is the content : {content}")
    
    response = call_api("columnNames", "get", params={"table_name": "files"})
    
    print(f"Column names : {response}")
    # for fname in params:
    #     print(params)
    #     response = call_api("file", params=params)
    #     # url = f"http://localhost:8080/file?filename={fname}&user_id={1}"
    #     # response = requests.get(url)
    #     if response:
    #         print(f"This is the content : {response.content}")
        # print(response.content.decode("utf-8").replace("\\n","\n"))
    # for file_name in params:
    #     # Check if the file exists in the current directory
    #     if fsDB.file_exists(file_name, current_pid):
    #         # Fetch the file contents from the database
    #         file_contents = fsDB.get_file_contents(file_name, current_pid)

    #         if file_contents is not None:
    #             # Check if the content is binary
    #             if isinstance(file_contents, bytes):
    #                 try:
    #                     # Try to decode the binary data as UTF-8 (text file)
    #                     decoded_contents = file_contents.decode('utf-8')
    #                     print(f"\nContents of {file_name}:\n{decoded_contents}\n")
    #                 except UnicodeDecodeError:
    #                     print(f"\nError: File '{file_name}' contains binary data and cannot be displayed as text.\n")
    #             else:
    #                 # If it's already a string, just print it
    #                 print(f"\nContents of {file_name}:\n{file_contents}\n")
    #         else:
    #             print(f"\nError: Could not read the contents of '{file_name}'.\n")
    #     else:
    #         print(f"\nError: File '{file_name}' does not exist in the current directory.\n")

    return ""
