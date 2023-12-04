import pandas as pd
import regex as re
import requests
from langdetect import detect, LangDetectException
from rijksdriehoek import rijksdriehoek

def clean_translate_reviews(input_file_path, urls_file_path, output_file_path, deepl_api_key):
    
    df = pd.read_csv(input_file_path)

    df.fillna('NA', inplace=True)
    
    # Cut specific time from the datetime
    if 'review_datetime_utc' in df.columns:
        df['review_datetime_utc'] = pd.to_datetime(df['review_datetime_utc']).dt.date
        
    urls_df = pd.read_csv(urls_file_path)
    
    # Merge the dataframes on the 'name' column from df and 'Location' column from urls_df
    df = df.merge(urls_df[['Location', 'Location_Unique', 'Status', 'Lat', 'Long']], 
                  left_on='name', 
                  right_on='Location', 
                  how='left')
    
    df.drop('Location', axis=1, inplace=True)
    
    # Define the emoji patternpip 
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons (smileys and emotion-related emojis)
        "\U0001F300-\U0001F5FF"  # Symbols and Pictographs (various symbols, weather icons, etc.)
        "\U0001F680-\U0001F6FF"  # Transport and Map Symbols (cars, trucks, maps, etc.)
        "\U0001F1E0-\U0001F1FF"  # Flags (country flags, regional indicators)
        "\U00002702-\U000027B0"  # Dingbats (decorative and miscellaneous symbols)
        "\U000024C2-\U0001F251"  # Enclosed Characters (circled letters, Japanese “here” button, etc.)
        "\U0001F700-\U0001F77F"  # Alchemical Symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs (including more emoticons and symbols)
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "]+", flags=re.UNICODE
    )

    # Define the text cleaning function
    def clean_review(text):
        if pd.isna(text):
            return pd.NA

        text = emoji_pattern.sub(r'', text)

        quote_pattern = re.compile(r'[\"“”„«»‹›]')
        text = quote_pattern.sub('', text)

        text = text.replace('…', '')

        return text
    
    # Clean the review_text column
    if 'review_text' in df.columns:
        df['review_text'] = df['review_text'].apply(clean_review)
        
    # Detect if text is English
    def is_english(text):
        try:
            return detect(text) == 'en'
        except LangDetectException:
            return False

    # Function to translate text using DeepL API
    def translate_text(text):
        if pd.isna(text) or is_english(text):
            return text

        url = "https://api-free.deepl.com/v2/translate"
        data = {
            'auth_key': deepl_api_key,
            'text': text,
            'target_lang': 'EN'
        }
        
        response = requests.post(url, data=data)
        return response.json()['translations'][0]['text']

    # Translate reviews
    if 'review_text' in df.columns:
        df['Translated_Review'] = df['review_text'].apply(translate_text)
    
    df.to_csv(output_file_path, index=False, na_rep='NA')

    print(f"Cleaned data saved to {output_file_path}")

def clean_water_quality(input_file_path, output_file_path):
    
    def convert_cor(x, y):

        rd = rijksdriehoek.Rijksdriehoek()
        rd.rd_x = x
        rd.rd_y = y
        lat, lon = rd.to_wgs()
    
        return lat, lon
    
    df = pd.read_csv(input_file_path)
    
    df.fillna('NA', inplace=True)
    
    # Cut specific time from the datetime and convert it to standard date format
    try:
        df['date'] = pd.to_datetime(df['datum'], format='%d-%m-%Y %H:%M').dt.date
    except ValueError:
        df['date'] = pd.to_datetime(df['datum'], dayfirst=True).dt.date

    # Apply the coordinate conversion function
    if 'locatie x' in df.columns and 'locatie y' in df.columns:
        df[['lat', 'lon']] = df.apply(lambda row: convert_cor(row['locatie x'], row['locatie y']), axis=1, result_type='expand')

    df.to_csv(output_file_path, index=False)

    print(f"Cleaned data saved to {output_file_path}")
    
def clean_weather(input_file_path, output_file_path):
    
    df = pd.read_csv(input_file_path, comment='#', delimiter=',')
    
    df.columns = df.columns.map(lambda x: x.strip())

    # Convert 'YYMMDD' to standard date format
    df['date'] = pd.to_datetime(df['YYYYMMDD'], format='%Y%m%d').dt.date
    
    daily_columns = ['date', 'FG', 'TG', 'SQ', 'DR', 'RH', 'PG', 'UG', 'EV24']
    df = df[daily_columns]
    
    columns_to_divide= ['FG', 'TG', 'SQ', 'DR', 'RH', 'PG', 'EV24']
    for col in columns_to_divide:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x / 10 if x != 0 else 0)

    df.to_csv(output_file_path, index=False)

    print(f"Cleaned data saved to {output_file_path}")