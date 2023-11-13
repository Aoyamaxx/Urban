import pandas as pd
import requests
from langdetect import detect, LangDetectException

# Load the CSV file
file = "by_newest_20231113_000949_1st"
df = pd.read_csv(f'1st_processed_reviews/{file}.csv', na_values='NA')

# Function to remove quotes
def remove_quotes(text):
    if pd.isna(text):
        return pd.NA
    
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    
    return text

def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False

# Function to translate text using DeepL API
def translate_text(row_number, text, auth_key):
    if pd.isna(text) or is_english(text):
        return text
    
    print(f"[{row_number}]: Translating: {text[:50]}...")
    
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        'auth_key': auth_key,
        'text': text,
        'target_lang': 'EN'
    }
    response = requests.post(url, data=data)
    return response.json()['translations'][0]['text']

# DeepL API Key
deepl_api_key = '631651fd-82bc-eca9-21cc-4861fe0a7a8f:fx' # From Xiao

# Translate reviews
df['Translated_Review'] = [translate_text(i, text, deepl_api_key) for i, text in enumerate(df['Review'].apply(remove_quotes), 1)]

# Write to new CSV file
df.to_csv(f'translated_reviews/{file}_translated.csv', index=False, na_rep='NA')

print(f"Done translating!")
