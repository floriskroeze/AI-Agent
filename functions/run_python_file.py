import os
import subprocess
from functions.get_absolute_and_target_path import get_absolute_and_target_path
from functions.is_valid_target_dir import is_valid_target_dir

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path, target_path = get_absolute_and_target_path(working_directory, file_path)

        if not is_valid_target_dir(abs_path, target_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        command = ["python", target_path]

        if args:
            command.extend(args)

        process = subprocess.run(command, capture_output=True, text=True, timeout=30.0)

        output = ""

        if not process.returncode == 0:
            output += f"Process exited with code {process.returncode}\n"
        
        if not process.stdout and not process.stderr:
            output += f" No output produced"
        elif not process.stderr: 
            output += f"STDOUT: {process.stdout}\n"
        else:
            output += f"STDERR: {process.stderr}\n"

        return output
    except Exception as e:
        return f"Error: {e}"