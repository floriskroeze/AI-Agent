import os

def is_valid_target_dir(absolute_path, target_path):
    return os.path.commonpath([absolute_path, target_path]) == absolute_path
