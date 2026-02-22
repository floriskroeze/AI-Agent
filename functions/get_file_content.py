import os
from functions.is_valid_target_dir import is_valid_target_dir
from functions.get_absolute_and_target_path import get_absolute_and_target_path
from google import genai

types = genai.types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Show first 10000 lines of file content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file from, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_path, target_path = get_absolute_and_target_path(working_directory, file_path)
        
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        if not is_valid_target_dir(abs_path, target_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        MAX_CHARS = 10000

        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'...File "{file_path}" truncated at {MAX_CHARS} characters'

            return file_content_string

    except Exception as e:
        return f'Error: {e}' 
