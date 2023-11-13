import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
# nltk.download('vader_lexicon')

file_path = 'final_cleaned_reviews/by_newest_20231113_000949_1st_translated_clean.csv'
data = pd.read_csv(file_path, encoding='utf-8', na_values='NA')

data = data[['Location_Unique', "Cleaned_Review", "Status"]].dropna()

sia = SentimentIntensityAnalyzer()

def get_sentiment_score(text):
    return sia.polarity_scores(text)['compound']

data['Sentiment_Score'] = data['Cleaned_Review'].apply(get_sentiment_score)

avg_sentiment = data.groupby('Location_Unique')['Sentiment_Score'].mean().reset_index()

print(avg_sentiment)

# Temperary visualization

avg_sentiment = avg_sentiment.set_index('Location_Unique')

# Join with status data
status_data = data[['Location_Unique', 'Status']].drop_duplicates().set_index('Location_Unique')
avg_sentiment = avg_sentiment.join(status_data)

# Calculate general average for official and unofficial locations
general_avg = data.groupby('Status')['Sentiment_Score'].mean()

# Plotting
plt.figure(figsize=(12, 8))
for status, color in [('official', 'skyblue'), ('unofficial', 'orange')]:
    subset = avg_sentiment[avg_sentiment['Status'] == status]
    plt.bar(subset.index, subset['Sentiment_Score'], color=color, label=f"{status} (Avg: {general_avg[status]:.2f})")

plt.xlabel('Location')
plt.ylabel('Average Sentiment Score')
plt.title('Average Sentiment Score by Location Status')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

