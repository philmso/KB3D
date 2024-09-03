import bpy
import os

# Get the current file path
current_file_path = bpy.data.filepath

# Check if the file is already saved
if current_file_path:
    # Get the directory of the current file
    directory = os.path.dirname(current_file_path)
    
    # Define the new file path with compression enabled
    save_path = os.path.join(directory, os.path.basename(current_file_path))
    
    # Save the current Blender file with compression enabled
    bpy.ops.wm.save_mainfile(filepath=save_path, compress=True)