# from .encoder_decoder import decode
from cmd_pkg.fs_state_manager import Fs_state_manager
from .call_api import call_api


def cat(params=None):
    """Display the contents of one or more files."""
    if not params:
        return {"status": "fail", "message": "\nError: No file specified."}

    filename = params[0]
    current_pid = Fs_state_manager.get_pid()
    oid = Fs_state_manager.get_oid()
    filters = {"name": filename, "pid": current_pid, "oid": oid}

    try:
        response = call_api("files", params=filters)

    except:
        return {"status": "fail", "message": "\nCould not make a call to the api"}

    if response:
        content = response[0]["contents"]

        if content == "":
            return {
                "status": "success",
                "message": f"\nThis file doesn't have any content inside it.",
            }

        else:
            return {"status": "success", "message": f"\n{content}"}

    return {"status": "fail", "message": "\nDidn't find the file you were looking for."}
