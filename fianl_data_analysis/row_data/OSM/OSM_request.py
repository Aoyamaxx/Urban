import pandas as pd
import requests
import json
import os
import shutil

def reset_output_OSM_data():

    output_dir_path = 'output_OSM_data'

    # Ask for user permission
    print("You are about to delete all files in the directory:", output_dir_path)
    choice = input("Enter 1 to continue, enter 0 to cancel, enter anything else to quit: ")

    if choice == '1':
        if os.path.exists(output_dir_path) and os.path.isdir(output_dir_path):
            for filename in os.listdir(output_dir_path):
                file_path = os.path.join(output_dir_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
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
        
    return

reset_output_OSM_data()

csv_file = '../reviews/urls.csv'
output_directory = 'output_OSM_data'
df = pd.read_csv(csv_file)

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# https://wiki.openstreetmap.org/wiki/Map_features
# Accsess above link to find the keys and values
# Tags list, where each item is a dictionary with 'key' and 'value'
tags = [
    {'key': 'public_transport', 'value': 'station'}, 
    {'key': 'amenity', 'value': 'parking'}, 
    {'key': 'amenity', 'value': 'toilets'}, 
    {'key': 'amenity', 'value': 'shower'}, 
    {'key': 'amenity', 'value': 'water_point'}, 
    {'key': 'amenity', 'value': 'drinking_water'}, 
    {'key': 'amenity', 'value': 'dressing_room'}, 
    {'key': 'amenity', 'value': 'bench'}, 
    {'key': 'amenity', 'value': 'lounger'}, 
    {'key': 'amenity', 'value': 'charging_station'},
    {'key': 'amenity', 'value': 'waste_basket'},
    {'key': 'amenity', 'value': 'ice_cream'},
    {'key': 'landuse', 'value': 'residential'},
    {'key': 'landuse', 'value': 'grass'},
    {'key': 'leisure', 'value': 'park'},
    {'key': 'shop', 'value': 'beverage'},
    {'key': 'shop', 'value': 'supermarket'},
    {'key': 'building', 'value': 'toilets'},
    {'key': 'emergency', 'value': 'lifeguard'}, 
    {'key': 'emergency', 'value': 'life_ring'}, 
    
    # {'key': 'leisure', 'value': 'playground'}, 
    ]

# Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"

# Function to create Overpass QL query for tags
def create_query(radius, lat, lon, tags_list):
    # Start the Overpass query
    query_parts = ['[out:json];']
    # Add query parts for each tag
    for tag in tags_list:
        query_parts.append(f'node[{tag["key"]}={tag["value"]}](around:{radius},{lat},{lon});')
        # Complete the query with output statement
        query_parts.append('out;')
    return ''.join(query_parts)

# Iterate over the dataframe rows
for index, row in df.iterrows():
    lat = row['Lat']
    lon = row['Long']
    location = row['Location'].replace("/", "_").replace(" ", "_")
    location_id = row['ID']
    radius = 500  # Radius in meters
    
    # Create the Overpass QL query for the specified tags
    overpass_query = create_query(radius, lat, lon, tags)
    
    # Print the query for debugging
    print(f"Query for location {location}: {overpass_query}")
    
    # Post the query to the Overpass API
    response = requests.post(overpass_url, data={'data': overpass_query})
    
    # Print the response for debugging
    print(f"Response from API: {response.text}")
    
    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()
        
        # Write the data to an output file
        output_file = os.path.join(output_directory, f"{location}_{location_id}.json")
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile)
    else:
        print(f"Failed to retrieve data for location {location}, HTTP status code {response.status_code}")

print("Data retrieval complete.")

