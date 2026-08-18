import os
from pathlib import Path

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Print the contents of the file",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {"type": "string","description": "Directory path of the absolute working directory"},
                "file_path": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        #print(target_file)
            
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
                
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string+= f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return file_content_string

        
    except Exception as e:
            return f"Error: {e}"
            
            
            