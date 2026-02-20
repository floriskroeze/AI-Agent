import os

def is_valid_target_dir(absolute_path, target_path):
    valid_target_dir = os.path.commonpath([absolute_path, target_path]) == absolute_path

    return valid_target_dir