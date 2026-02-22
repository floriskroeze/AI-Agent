import os
from functions.is_valid_target_dir import is_valid_target_dir
from functions.get_absolute_and_target_path import get_absolute_and_target_path
from google import genai

types = genai.types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes conten to file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file from, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try: 
        abs_path, target_path = get_absolute_and_target_path(working_directory, file_path)

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{target_path}" as it is a directory'

        if not is_valid_target_dir(abs_path, target_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)

        with open(target_path, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'