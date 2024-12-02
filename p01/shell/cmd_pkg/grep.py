from .call_api import call_api
from .fs_state_manager import Fs_state_manager
import re

def grep(params=None, input=None):
    if (params == None and input == None):
        return {
            "status": "fail",
            "message": "\nPlease specify the pattern and the filename"
        }
    elif len(params) == 1 and input == None:
        return {
            "status": "fail",
            "message": "\nPlease specify the pattern first and file after that."
        }
    elif len(params) > 2:
        return {
            "status": "fail",
            "message": "\nToo manyu parameters."
        }
    elif input is not None and len(params) == 0:
        return {
            "status": "fail",
            "message": "\nPlease specify the pattern"
        }
    
    pattern = params[0]
    contents = ""
    message = ""

    if input == None:
        filename = params[1]
        oid = Fs_state_manager.get_oid()
        pid = Fs_state_manager.get_pid()
        
        filters = {"oid": oid, "pid": pid, "name": filename}
        
        try:
            response = call_api("files", params=filters)

            if response["status"] == "success":
                contents = response["message"][0]["contents"]
            
            else:
                return {
                    "status": "fail",
                    "message": f"\nFile '{filename}' doesn't exist."
                }
        except:
            return {
                "status": "fail",
                "message": "\nCannot make a call to api."
            }
    else:
        contents = input["message"]
    
    lines = contents.split("\n")

    for line in lines:
        result = bool(re.search(pattern, line))
        
        if result == True:
            message += "\n"+line
    
    return {
        "status": "success",
        "message": message
    }
    