# Use this script to reset the output directory to a clean state.
import os
import shutil

output_dir_path = 'output_OSM_data'

# Ask for user permission
print("You are about to delete all files in the directory:", output_dir_path)
choice = input("Enter 1 to continue, enter 0 to cancel, enter anything else to quit: ")

if choice == '1':
    # Check if the directory exists
    if os.path.exists(output_dir_path) and os.path.isdir(output_dir_path):
        # List all files in the directory
        for filename in os.listdir(output_dir_path):
            file_path = os.path.join(output_dir_path, filename)
            try:
                # If it's a file, delete it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # If it's a directory, delete it and all its contents
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        print(f"All files in {output_dir_path} have been deleted.")
    else:
        print(f"The directory {output_dir_path} does not exist.")
elif choice == '0':
    print("Operation cancelled by user.")
else:
    print("Invalid input. Operation quit.")
