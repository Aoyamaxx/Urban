import pandas as pd
import json
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def calculate_amenity_scores(input_file_path, output_file_path, data_folder):
    
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
    
    locations_df = pd.read_csv(input_file_path)
    locations = locations_df['Location']

    scores = []

    for i, location in enumerate(locations):
        # Construct the JSON filename
        filename = f"{data_folder}/{location.replace(' ', '_')}_{i+1}.json"

        # Read JSON file
        try:
            with open(filename, 'r') as file:
                data = json.load(file)

            # Calculate the score for each location
            score = calculate_amenity_score(data)
            scores.append(score)
        except FileNotFoundError:
            print(f"File not found: {filename}")
            scores.append(0)

    # Normalize the scores
    normalized_scores = normalize_scores(scores)

    # Create a DataFrame for output
    output_df = pd.DataFrame({
        'Location': locations,
        'Amenities_Score': scores,
        'Normalized_Amenities_Score': normalized_scores
    })

    output_df.to_csv(output_file_path, index=False)
    
    print(f"Amenity scores saved to: {output_file_path}")

def compute_sentiment_scores(input_file_path, output_file_path):
    
    def preprocess_text(text):
        if pd.isna(text):
            return pd.NA
        text = text.lower()  # Normalize case
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'@\S+', '', text)  # Remove usernames
        text = ' '.join(text.split())  # Correct whitespace
        return text
    
    df = pd.read_csv(input_file_path, na_values='NA')

    df['Cleaned_Review'] = df['Translated_Review'].apply(preprocess_text)

    # Initialize VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Get sentiment score
    def get_sentiment_score(text):
        if pd.isna(text):
            return pd.NA
        return sia.polarity_scores(text)['compound']

    df['Sentiment_Score'] = df['Cleaned_Review'].apply(get_sentiment_score)

    df.to_csv(output_file_path, index=False)

    print(f"Sentiment scores computed and saved to {output_file_path}")