class CWDManager:
    def __init__(self):
        self.cwd = ["~"]  # Start at home directory by default
    
    def set_path(self, new_path):
        if new_path == "~":  # Home directory
            self.cwd = ["~"]
        elif new_path.startswith("/"):
            # Absolute path, so reset the path
            self.current_path = new_path.split("/")
        else:
            # Relative path, modify the current path
            for part in new_path.split("/"):
                if part == "..":
                    if len(self.current_path) > 1:
                        self.current_path.pop()  # Go back one directory
                elif part != "." and part:
                    self.current_path.append(part)  # Move to a subdirectory

    def get_path(self):
        return "/" + "/".join(self.cwd) if self.cwd != ["~"] else "~"
    
cwd_manager = CWDManager()