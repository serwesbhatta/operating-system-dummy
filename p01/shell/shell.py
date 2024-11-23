import os, sys

# Add the parent directory to the system path to import 'database'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ensure fsDB is available, import it from your main API or initialize it
from database.sqliteCRUD import SqliteCRUD

from time import sleep
import importlib
import pkgutil
import cmd_pkg

# Import the Write_file function from your API
from api.routes.write_file import Write_file

#  Import commands
from cmd_pkg import *

from cmd_pkg.call_api.call_api import call_api
from cmd_pkg.fs_state_manager import Fs_state_manager
from cmd_pkg.file_path_helper import file_path_helper

# Initialize your database connection (you may need to update this path)
fsDB = SqliteCRUD("../database/data/filesystem.db")

# Dictionary to store the commands
cmds = {}


##################################################################################
##################################################################################

getch = Getch()  # create instance of our getch class

# Get the prompt string
# prompt = prompt()

# Used as a pointer in the terminal
# ppointer = {
#     "current_path" : "/",
#     "current_dir" : "/",
#     "pid" : "1",
#     "old" : "1"
# }

def print_cmd(cmd):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r" + padding)
    sys.stdout.write("\r" + cmd_pkg.prompt() + cmd)
    sys.stdout.flush()

# Dynamically load all functions from cmd_pkg into the dictionary
def load_commands():
    global cmds

    # Loop through all modules in the cmd_pkg package
    for _, module_name, _ in pkgutil.iter_modules(cmd_pkg.__path__):
        module = importlib.import_module(f"cmd_pkg.{module_name}")

        # Loop through the attributes in each module
        for name in dir(module):
            obj = getattr(module, name)
            # Check if it's a callable function and doesn't start with '__'
            if callable(obj) and not name.startswith("__"):
                cmds[name] = obj

# # Function to get flags
# def get_flags(args):
    

# Helper function to execute a single command
def execute_command(main_cmd, args, input_data=None):
    if main_cmd in cmds:
        # Check if the command can accept input data and provide it if available
        if input_data is not None and 'accepts_input' in cmds[main_cmd]:
            result = cmds[main_cmd](params=args, input=input_data)
        else:
            result = cmds[main_cmd](params=args) if args else cmds[main_cmd]()
        return result
    else:
        return {
            "message": f"Error: Command '{main_cmd}' not found."
        }

if __name__ == "__main__":
    # Load the commands dynamically from cmd_pkg
    load_commands()
    arrow_count = -1
    cmd = ""  # empty cmd variable
    cursor_position = len(cmd) 

    print_cmd(cmd)  # print to terminal
    # cmd_pkg.history(None)
    while True:  # loop forever

        char = getch()  # read a character (but don't print)

        if char == "\x03" or cmd == "exit":  # ctrl-c
            raise SystemExit("\nBye.")

        elif char == "\x7f":  # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)

        elif char in "\x1b":  # arrow key pressed
            null = getch()  # waste a character
            direction = getch()  # grab the direction
            history_response = cmd_pkg.history(None)
            history_contents = history_response["message"].split('\n')  # split history into lines
            if direction in "A":  # up arrow pressed
        # check if arrow_count is within the valid range of history
                if arrow_count < len(history_contents) - 1:
                    arrow_count += 1
                    # get the command from history, considering how far back we are (arrow_count)
                    history_command = history_contents[-(arrow_count + 1)].strip()
                    # update the current command (cmd) with the selected history command
                    cmd = history_command.split(maxsplit=1)[-1] if ' ' in history_command else history_command
                    print_cmd(cmd)
                else:
                    print("\nNo more history.\n")

            if direction in "B":  # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                # Check if we can move down in the history
                if arrow_count > 0:
                    arrow_count -= 1
            # Get the command for the current position in history after decrement
                    if arrow_count < len(history_contents):
                        history_command = history_contents[-(arrow_count + 1)].strip()

                        # Update the current command (cmd) with the selected history command
                        cmd = history_command.split(maxsplit=1)[-1] if ' ' in history_command else history_command
                        print_cmd(cmd)
                    else:
                    # If we're at the end of history, clear the command
                        cmd = ""
                        print_cmd(cmd)  # Clear the command display
                else:
                    cmd = ""
                    print_cmd("")


            if direction in "C":  # right arrow pressed
                if cursor_position < len(cmd):  # Ensure we don't go past the end of the command
                    cursor_position += 1
                    print("\x1b[C", end="", flush=True)  # Move the cursor right

            if direction in "D":  # left arrow pressed
                if cursor_position > 0:  # Ensure we don't go past the start of the command
                    cursor_position -= 1  # Move cursor one position back
                    print("\x1b[D", end="", flush=True)  # Move the cursor left

        elif char in "\r":  # return pressed
            arrow_count = -1
            # # This 'elif' simulates something "happening" after pressing return
            # print_cmd("Executing command....")
            # sleep(1)
            if cmd:
                cmd_pkg.history(cmd)

                commands = cmd
                redirection = False
                redirection_file_path = ""

                if ">" in cmd:
                    tokens = cmd.split(">")
                    commands = tokens[0].strip()
                    redirection_file_path = tokens[1].strip()
                    redirection = True

                if "|" in cmd:
                    input_data = None
                    each_commands = commands.split("|")

                    for index, each_command in enumerate(each_commands):
                        each_command = each_command.strip().split()
                        each_command_main = each_command[0]
                        each_command_args = each_command[1:]
                        
                        result = execute_command(each_command_main, each_command_args, input_data)

                        if "Error" in result["message"]:
                            print(result["message"])
                            break

                        input_data = result

                        if index == len(each_commands) - 1:
                            print(result["message"])
                else:
                    command = commands.strip().split()
                    main_cmd = command[0]
                    cmd_args = command[1:]

                    result = execute_command(main_cmd, cmd_args) 
                    
                    print(result["message"])

                    if redirection:
                        content = result["message"]

                        try:
                            path_response = file_path_helper(redirection_file_path)

                            if path_response["directories_exist"]:
                                oid = path_response["oid"]
                                pid = path_response["pid"]
                                redirection_file = path_response["file_name"]
                                redirection_filters = {
                                    "oid": oid,
                                    "pid": pid,
                                    "filepath": redirection_file,
                                    "content": content
                                }

                        except:
                            print("Cannot resolve path successfully.")

                        try:
                            response = call_api("write", "put", data=redirection_filters)

                            if response["status"] == "success":
                                print(response["message"])
                            else:
                                print(f"Failed to write to file {redirection_file_path}")
                        except:
                            print("Can't process the redirection request.")
            else:
                # If there is no cmd then print the prompt in a new line
                print("\n")

            # Check for pipes
            # if "|" in cmd:
            #     # Split by pipes
            #     pipe_cmds = cmd.split("|")
                
            #     input_data = None  # This will store the output from the previous command

            #     for pipe_cmd in pipe_cmds:
            #         # Split the subcommand and its arguments
            #         cmd_parts = pipe_cmd.strip().split()
                    
            #         if len(cmd_parts) > 0:
            #             main_cmd = cmd_parts[0]
            #             args = cmd_parts[1:]

            #             # Execute the command
            #             result = execute_command(main_cmd, args, input_data)
                        
            #             # If result is an error, stop processing further
            #             if "Error" in result:
            #                 print(result)
            #                 break
                        
            #             # Pass the result as input for the next command
            #             input_data = result

            #     # Handle output redirection if applicable
            #     if ">" in cmd:
            #         output_file = cmd.split(">")[-1].strip()

            #         user_id = 1 #TODO: use dynamic value
            #         api_response = Write_file(fsDB, output_file, input_data, user_id)

            #          # Check if the API succeeded in writing to the database
            #         if api_response.get("message"):
            #             print(f"\n{api_response['message']}")
            #         else:
            #             print(f"\nError: Could not write to the file '{output_file}'.")

            #     else:
            #         # No redirection, just print the output of the command
            #         print(f"\n{input_data}")

            # else:
            #     # No pipe, execute normally
            #     cmd_parts = cmd.split()

            #     if len(cmd_parts) > 0:
            #         main_cmd = cmd_parts[0]
            #         args = cmd_parts[1:]

            #         if main_cmd in cmds:
            #             # Call the function
            #             result = cmds[main_cmd](params=args) if args else cmds[main_cmd]()
                        
            #             # Handle output redirection if applicable
            #             if ">" in cmd:
            #                 output_file = cmd.split(">")[-1].strip()
                            
            #                 # Use the Write_file API to write the result to the database file system
            #                 user_id = 1  # Assuming static user ID
            #                 api_response = Write_file(fsDB, output_file, result, user_id)

            #                 if api_response.get("message"):
            #                     print(f"\n{api_response['message']}")
            #                 else:
            #                     print(f"\nError: Could not write to the file '{output_file}'.")
                        
            #             else:
            #                 # No redirection, just print the result
            #                 print(f"\n{result}")
            #         else:
            #             print(f"\nError: Command '{main_cmd}' not found.")

            ## YOUR CODE HERE
            ## Parse the command
            ## Figure out what your executing like finding pipes and redirects

            cmd = ""  # reset command to nothing (since we just executed it)
            print_cmd(cmd)  # now print empty cmd prompt
        else:
            cmd += char  # add typed character to our "cmd"
            print_cmd(cmd)  # print the cmd out



# Get the docstring of a function
def get_docstring(func_name):
    if func_name in cmds:
        return cmds[func_name].__doc__
    else:
        return f"Function '{func_name}' not found."