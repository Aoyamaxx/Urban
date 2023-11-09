import os
import re

def filter_files_by_id(directory, location_id):
    # Compile a regex pattern that looks for an underscore, the location_id, and the .json extension
    pattern = re.compile(rf"_{location_id}\.json$")
    
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter files that end with the specified location_id
    filtered_files = [file for file in files if pattern.search(file)]
    
    return filtered_files


directory_path = 'output_OSM_data'
location_id = 8
matching_files = filter_files_by_id(directory_path, location_id)
print(matching_files)