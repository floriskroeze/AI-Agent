import os

def is_valid_target_dir(absoplute_path, target_path):
    return os.path.commonpath([absoplute_path, target_path]) == absoplute_path
