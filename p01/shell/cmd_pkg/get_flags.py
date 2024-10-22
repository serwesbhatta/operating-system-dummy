def get_flags(args = None):
  flags = []

  if args:
    for arg in args:
      if arg.startswith('-'):
        # if flag contains multiple characters, slipt them up
        for char in arg[1:]:
          flags.append(char)

  return flags
