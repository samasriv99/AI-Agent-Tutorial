import os
from pathlib import Path

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write to a specified file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the specified python file that needs to be executed",
                },
                "working_directory": {"type": "string","description": "Directory path of the absolute working directory"},
                #"args":{"type":"list", "description": "Optional arguments to run the python file"},
                "content": {"type": "string", "description": "the content to write to a file"},
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        os.makedirs(file_path, exist_ok=True)
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        #print(target_file)
                
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
                    
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        
    
        MAX_CHARS = 10000
        with open(target_file, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
            
    except Exception as e:
        return f"Error: {e}"
