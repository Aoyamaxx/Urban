import pandas as pd
import re

file = 'by_newest_20231113_000949_1st_translated'
file_path = f'../../gmr_scraper/translated_reviews/{file}.csv'

df = pd.read_csv(file_path)

# Function for text preprocessing
def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()  # Normalize case
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\S+', '', text)  # Remove usernames
    text = ' '.join(text.split())  # Correct whitespace
    return text

# Apply preprocessing to the Translated_Review column
df['Cleaned_Review'] = df['Translated_Review'].apply(preprocess_text)

# Save the cleaned data to a new CSV file
cleaned_file_path = f'final_cleaned_reviews/{file}_clean.csv'  # Replace with your desired file path
df.to_csv(cleaned_file_path, index=False)

print(f"Cleaned data saved to {cleaned_file_path}")