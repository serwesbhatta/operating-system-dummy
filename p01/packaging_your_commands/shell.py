import os
import sys
from time import sleep
from cmd_pkg import *
import importlib
import pkgutil
import cmd_pkg

# Dictionary to store the commands
cmds = {}


##################################################################################
##################################################################################

getch = Getch()  # create instance of our getch class

# Get the prompt string
prompt = prompt()

def print_cmd(cmd):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r" + padding)
    sys.stdout.write("\r" + prompt + cmd)
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

if __name__ == "__main__":
    # Load the commands dynamically from cmd_pkg
    load_commands()

    cmd = ""  # empty cmd variable

    print_cmd(cmd)  # print to terminal

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

            # Split the input command at the first ">"
            cmd, output_file = cmd.split(">", 1) if ">" in cmd else (cmd, "")

            # Remove spaces
            cmd = cmd.strip()
            output_file = output_file.strip() if output_file else ""

            # Split commands and the arguments
            cmd_parts = cmd.split()

            if len(cmd_parts) > 0:
                main_cmd = cmd_parts[0]
                args = cmd_parts[1:]

                if main_cmd in cmds:
                    # Call the function
                    result = cmds[main_cmd](params=args) if args else cmds[main_cmd]()
                
                    if output_file:
                        with open(output_file, "w") as f:
                            f.write(result)
                    
                    else:
                        print(f"\n{result}")
            
                else:
                    print()
                    print(f"Error: Command '{main_cmd}' not found.")
            
            cmd =""
            print_cmd(cmd)
            
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
