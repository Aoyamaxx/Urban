import pandas as pd
import json

def calculate_amenity_score(amenities_data):
    # List of amenities to check with their respective key-value pairs
    amenities = [
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
    ]
    score = 0
    for amenity in amenities:
        for element in amenities_data['elements']:
            tags = element.get('tags', {})
            if tags.get(amenity['key']) == amenity['value']:
                score += 1
                break
    return score


def normalize_scores(scores):
    amenities = [
        'public_transport', 'parking', 'toilets', 'shower', 'water_point',
        'drinking_water', 'dressing_room', 'bench', 'lounger', 'charging_station',
        'waste_basket', 'ice_cream', 'restaurant', 'cafe'
    ]
    max_score = len(amenities)
    return [round(score / max_score, 2) for score in scores]

# Get locations
locations_df = pd.read_csv('../gmr_scraper/input/urls.csv')
locations = locations_df['Location']

scores = []

for i, location in enumerate(locations):
    # Construct the JSON filename
    filename = f"output_OSM_data/{location.replace(' ', '_')}_{i+1}.json"

    # Read JSON file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Calculate the score for each location
    score = calculate_amenity_score(data)
    scores.append(score)

# Normalize the scores
normalized_scores = normalize_scores(scores)

# Create a DataFrame for output
output_df = pd.DataFrame({
    'Location': locations,
    'Score': scores,
    'Normalized Score': normalized_scores
})

output_df.to_csv('amenities_scores_results/amenities_scores.csv', index=False)

print("Done!")