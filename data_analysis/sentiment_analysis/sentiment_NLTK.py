import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
# nltk.download('vader_lexicon')

file_path = 'final_cleaned_reviews/by_newest_20231113_000949_1st_translated_clean.csv'
data = pd.read_csv(file_path, encoding='utf-8', na_values='NA')

data = data[['Location_Unique', "Cleaned_Review"]].dropna()

sia = SentimentIntensityAnalyzer()

def get_sentiment_score(text):
    return sia.polarity_scores(text)['compound']

data['Sentiment_Score'] = data['Cleaned_Review'].apply(get_sentiment_score)

avg_sentiment = data.groupby('Location_Unique')['Sentiment_Score'].mean().reset_index

print(avg_sentiment)
