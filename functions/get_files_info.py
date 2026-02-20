import os
from functions.is_valid_target_dir import is_valid_target_dir

def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, directory))
    
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        if not is_valid_target_dir(abs_path, target_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        dir_contents = ""

        for item in os.scandir(target_path):
            size = os.stat(item).st_size

            dir_contents += f"- {item.name}: file_size:{size} bytes, is_dir={item.is_dir()}\n"

        return dir_contents
    except Exception as e:
        return f'Error listing files: {e}'
    
