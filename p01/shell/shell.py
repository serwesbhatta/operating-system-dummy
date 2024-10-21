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

# Initialize your database connection (you may need to update this path)
fsDB = SqliteCRUD("../database/data/filesystem.db")

# Dictionary to store the commands
cmds = {}


##################################################################################
##################################################################################

getch = Getch()  # create instance of our getch class

# Get the prompt string
# prompt = prompt()

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

# Helper function to execute a single command
def execute_command(main_cmd, args, input_data=None):
    if main_cmd in cmds:
        # Call the function with or without parameters
        result = cmds[main_cmd](params=args) if args else cmds[main_cmd]()
        return result
    else:
        return f"Error: Command '{main_cmd}' not found."

if __name__ == "__main__":
    # Load the commands dynamically from cmd_pkg
    load_commands()

    cmd = ""  # empty cmd variable

    print_cmd(cmd)  # print to terminal
    cmd_pkg.history(None)
    while True:  # loop forever

        char = getch()  # read a character (but don't print)

        if char == "\x03" or cmd == "exit":  # ctrl-c
            raise SystemExit("Bye.")

        elif char == "\x7f":  # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)

        elif char in "\x1b":  # arrow key pressed
            null = getch()  # waste a character
            direction = getch()  # grab the direction

            if direction in "A":  # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)
                cmd += "\u2191"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "B":  # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                cmd += "\u2193"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "C":  # right arrow pressed
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                cmd += "\u2192"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "D":  # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                cmd += "\u2190"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            print_cmd(cmd)  # print the command (again)

        elif char in "\r":  # return pressed

            # # This 'elif' simulates something "happening" after pressing return
            # print_cmd("Executing command....")
            # sleep(1)
            cmd_pkg.history(cmd)
            # Check for pipes
            if "|" in cmd:
                # Split by pipes
                pipe_cmds = cmd.split("|")
                
                input_data = None  # This will store the output from the previous command

                for pipe_cmd in pipe_cmds:
                    # Split the subcommand and its arguments
                    cmd_parts = pipe_cmd.strip().split()
                    
                    if len(cmd_parts) > 0:
                        main_cmd = cmd_parts[0]
                        args = cmd_parts[1:]

                        # Execute the command
                        result = execute_command(main_cmd, args, input_data)
                        
                        # If result is an error, stop processing further
                        if "Error" in result:
                            print(result)
                            break
                        
                        # Pass the result as input for the next command
                        input_data = result

                # Handle output redirection if applicable
                if ">" in cmd:
                    output_file = cmd.split(">")[-1].strip()

                    user_id = 1 #TODO: use dynamic value
                    api_response = Write_file(fsDB, output_file, input_data, user_id)

                     # Check if the API succeeded in writing to the database
                    if api_response.get("message"):
                        print(f"\n{api_response['message']}")
                    else:
                        print(f"\nError: Could not write to the file '{output_file}'.")

                else:
                    # No redirection, just print the output of the command
                    print(f"\n{input_data}")

            else:
                # No pipe, execute normally
                cmd_parts = cmd.split()

                if len(cmd_parts) > 0:
                    main_cmd = cmd_parts[0]
                    args = cmd_parts[1:]

                    if main_cmd in cmds:
                        # Call the function
                        result = cmds[main_cmd](params=args) if args else cmds[main_cmd]()
                        
                        # Handle output redirection if applicable
                        if ">" in cmd:
                            output_file = cmd.split(">")[-1].strip()
                            
                            # Use the Write_file API to write the result to the database file system
                            user_id = 1  # Assuming static user ID
                            api_response = Write_file(fsDB, output_file, result, user_id)

                            if api_response.get("message"):
                                print(f"\n{api_response['message']}")
                            else:
                                print(f"\nError: Could not write to the file '{output_file}'.")
                        
                        else:
                            # No redirection, just print the result
                            print(f"\n{result}")
                    else:
                        print(f"\nError: Command '{main_cmd}' not found.")

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