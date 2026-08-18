import os
from pathlib import Path

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists the metadata of files of a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
                "working_directory": {"type": "string","description": "Directory path of the absolute working directory"},
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        
        output = [f'Success: "{directory}" is within the working directory']
        
        if directory == ".":
            directory = "current"
            
        output.append(f"Results for the '{directory}' directory:")
        
        
        dir_items = os.listdir(target_dir)
        #output.append(str(dir_items))
        
        for item in dir_items:
            
            item_path = os.path.join(target_dir, item)
            
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            
            output.append(f"    -{item}: file_size={size}, is_dir={is_dir}")

       
        return "\n".join(output)

    except Exception as e:
        return f"Error: {e}"


#print(get_files_info("calculator", "."))
   
