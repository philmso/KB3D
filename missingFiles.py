import bpy
import os

# Function to get the directory of the current .blend file
def get_blend_directory():
    return os.path.dirname(bpy.data.filepath)

# Function to get the Textures folder path based on the .blend file
def get_textures_folder():
    blend_file_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]  # Get the blend file name without extension
    textures_folder = os.path.join(get_blend_directory(), f"{blend_file_name} Textures")
    return textures_folder

# Function to check if the file exists in the Textures folder
def file_exists_in_textures_folder(filepath):
    textures_folder = get_textures_folder()
    file_name = os.path.basename(filepath)  # Extract the file name
    search_path = os.path.join(textures_folder, file_name)
    return os.path.exists(search_path), search_path

# Function to check if any files are missing
def check_for_missing_files():
    missing_files = []

    # Check images (textures)
    for img in bpy.data.images:
        if img.source == 'FILE' and img.filepath:
            if not os.path.exists(bpy.path.abspath(img.filepath)):
                missing_files.append((img.name, img.filepath))

    # Check linked libraries
    for lib in bpy.data.libraries:
        if lib.filepath:
            if not os.path.exists(bpy.path.abspath(lib.filepath)) and lib.filepath != "":
                missing_files.append((lib.name, lib.filepath))

    return missing_files

# Function to find and fix missing files in the Textures folder
def find_and_fix_missing_files(missing_files):
    for name, filepath in missing_files:
        exists, new_path = file_exists_in_textures_folder(filepath)
        if exists:
            # Update the file path to the correct location
            if isinstance(bpy.data.images.get(name), bpy.types.Image):
                bpy.data.images[name].filepath = bpy.path.relpath(new_path)
            elif isinstance(bpy.data.libraries.get(name), bpy.types.Library):
                bpy.data.libraries[name].filepath = bpy.path.relpath(new_path)
            print(f"Updated: {name} -> {new_path}")
        else:
            print(f"Could not find: {name} in Textures folder.")

# Main function
def main():
    print("Checking for missing files...")

    # Check for missing files
    missing_files = check_for_missing_files()

    if missing_files:
        print("Missing files found. Attempting to fix them...")
        find_and_fix_missing_files(missing_files)
        print("Finished fixing missing files.")
        
        # Save the current .blend file
        bpy.ops.wm.save_mainfile()
    else:
        print("No missing files detected. No action taken.")

# Run the main function
main()
