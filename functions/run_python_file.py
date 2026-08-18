import os
import subprocess
from pathlib import Path

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes the specified python script",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the specified python file that needs to be executed",
                },
                "working_directory": {"type": "string","description": "Directory path of the absolute working directory"},
                "args":{"type":"list", "description": "Optional arguments to run the python file"},
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        #os.makedirs(file_path, exist_ok=True)
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        #print(target_file)
                
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                    
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        n = len(file_path)
        if file_path[n-3:n:1]!=".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        cp = subprocess.run(command, cwd = abs_working_dir, capture_output=True, text=True,timeout=30)
        output = ""
        if cp.returncode!=0:
            output+="Process exited with code X"
        elif not cp.stdout and not cp.stderr:
            output+="No output produced"
        else:
            if cp.stdout:
                output+=f"STDOUT: {cp.stdout}"
            if cp.stderr:
                output+=f"STDERR:{cp.stderr}"
        return output
        


        
    
       
    
            
    except Exception as e:
        return f"Error: executing Python file: {e}"