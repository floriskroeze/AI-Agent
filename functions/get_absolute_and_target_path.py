import os

def get_absolute_and_target_path(working_dir, path):
    abs_path = os.path.abspath(working_dir)
    target_path = os.path.normpath(os.path.join(abs_path, path))
    
    return abs_path, target_path