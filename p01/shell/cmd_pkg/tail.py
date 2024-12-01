from .call_api import call_api
from .fs_state_manager import Fs_state_manager


def tail(params):
    """Display the first N lines of a file."""
    if params == None or len(params) < 1:
        return {"status": "fail", "message": "\nError: No file specified."}

    file_name = params[0]
    num_lines = 10  # Default to 10 if no -n option is provided

    # Check if -n option is provided
    if len(params) == 3 and params[1] == "-n":
        try:
            num_lines = int(params[2])
            if num_lines < 1:
                return {
                    "status": "fail",
                    "message": "\nError: Number of lines must be a positive integer.",
                }
        except ValueError:
            return {
                "status": "fail",
                "message": "\nError: Invalid number of lines specified. It must be an integer.",
            }
    elif len(params) > 1 and params[1] != "-n":
        return {
            "status": "fail",
            "message": "\nError: Invalid command format. Use -n followed by a number.",
        }

    elif len(params) > 3:
        return {"status": "fail", "message": "\nError: Too many parameters passed."}

    pid = Fs_state_manager.get_pid()
    oid = Fs_state_manager.get_oid()

    filters = {"oid": oid, "pid": pid, "name": file_name}

    try:
        response = call_api("files", params=filters)

        # Fetch file contents from the database
        if response["status"] == "success":
            file_contents = response["message"][0]["contents"]

            if file_contents is not None:
                lines = file_contents.split("\n")
                message = "\n".join(lines[-num_lines:])
                return {"status": "success", "message": message}
            else:
                return {
                    "status": "fail",
                    "message": f"\nError: Could not read the contents of '{file_name}'.",
                }
        else:
            return {
                "status": "fail",
                "message": f"\nError: File '{file_name}' does not exist in the current directory.",
            }
    except:
        return {"status": "fail", "message": "\nCould not make a call to api"}
