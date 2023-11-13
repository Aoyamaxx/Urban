import regex as re
import pandas as pd

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
    "]+", flags=re.UNICODE)

def clean_review(text):
    if pd.isna(text):
        return pd.NA
    
    text = emoji_pattern.sub(r'', text)
    
    quote_pattern = re.compile(r'[\"“”„«»‹›]')
    text = quote_pattern.sub('', text)
    
    text = text.replace('…', '')
        
    return text

file = "by_newest_20231113_000949"
file_name = f"{file}.csv"
file_path = f'output/{file_name}'
df = pd.read_csv(file_path, na_values='NA')

# Apply the cleaning function to the 'Review' column
df['Review'] = df['Review'].apply(clean_review)

# Save the cleaned DataFrame to a new CSV file
df.to_csv(f'1st_processed_reviews/{file}_1st.csv', index=False, na_rep='NA')

print(f"Done cleaning!")