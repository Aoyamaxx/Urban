import requests

GOOGLE_MAPS_API_KEY = 'AIzaSyBTNBrRNkhtALl6z24nX_ySG9OfQFhvq3w'  # Replace with your Google Maps API key
WEXTRACTOR_API_KEY = '5949b9c7cf3deb0e96a1a2c6c9b443b79b5143e5'  # Replace with your Wextractor API key

def get_place_id(search_query):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': search_query,
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get(endpoint_url, params=params).json()

    if 'status' in response and response['status'] != 'OK':
        print(response.get('error_message', 'Unknown error'))
        return None

    return response['results'][0]['place_id'] if 'results' in response and len(response['results']) > 0 else None

def get_google_maps_reviews(place_id, offset):
    endpoint_url = "https://wextractor.com/api/v1/reviews"
    params = {
        "auth_token": WEXTRACTOR_API_KEY,
        "id": place_id,
        "offset": offset
    }
    
    response = requests.get(endpoint_url, params=params)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None
    
    data = response.json()
    return data.get('reviews', [])

def write_reviews_to_file(reviews):
    with open('reviews.txt', 'a') as file:
        for review in reviews:
            author = review.get('author', 'N/A')
            rating = review.get('rating', 'N/A')
            text = review.get('text', 'N/A')
            
            file.write(f"Author: {author}\n")
            file.write(f"Rating: {rating}\n")
            file.write(f"Text: {text}\n\n")

if __name__ == "__main__":
    place_name = input("Enter the name of the place: ")
    place_id = get_place_id(place_name)
    
    if place_id:
        print(f"Place ID for {place_name}: {place_id}")
        
        offset = 0
        while True:
            reviews = get_google_maps_reviews(place_id, offset)
            if not reviews:
                print(f"No more reviews found for the place with ID: {place_id} at offset: {offset}")
                break  # Exit the loop if no more reviews are found
            
            write_reviews_to_file(reviews)  # Append the reviews to the text file
            
            print(f"Reviews written for offset: {offset}")
            offset += 10  # Increment the offset for the next iteration
    else:
        print(f"No place ID found for {place_name}.")
