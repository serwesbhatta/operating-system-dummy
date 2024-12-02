def get_flags(args=None):
    flags = []
    flags_index = []

    if args:
        for index, arg in enumerate(args):
            if arg.startswith("-"):
                # Record the index of this flag
                flags_index.append(index)
                # If the flag contains multiple characters, split them up
                for char in arg[1:]:
                    flags.append(char)

    return {
        "flags": flags, 
        "flags_index": flags_index
        }
