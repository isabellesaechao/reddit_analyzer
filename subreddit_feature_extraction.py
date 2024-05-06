"""
Analyzes the features of the hot posts from the subredit using TD-IDF
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data/valorant_data.csv')

# Assuming 'text' is the column containing the text data
data = df['entire_post_text'].astype(str).tolist()

# Create a TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=20)  # Adjust parameters as needed

# Fit and transform the documents
tfidf_matrix = vectorizer.fit_transform(data)

# Get feature names (terms) from the vectorizer
feature_names = vectorizer.get_feature_names_out()

# Create a DataFrame to display the TF-IDF results
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

# Sum the TF-IDF scores across all documents to get a global importance score for each term
global_tfidf_scores = tfidf_matrix.sum(axis=0).A1

# Create a DataFrame to store the global TF-IDF scores
global_tfidf_df = pd.DataFrame({'Term': feature_names, 'TF-IDF Score': global_tfidf_scores})

# Sort the DataFrame by TF-IDF scores in descending order
global_tfidf_df = global_tfidf_df.sort_values(by='TF-IDF Score', ascending=False)

# Create a bar chart to visualize the TF-IDF scores
plt.figure(figsize=(10, 6))
plt.barh(global_tfidf_df['Term'], global_tfidf_df['TF-IDF Score'], color='skyblue')
plt.xlabel('TF-IDF Score')
plt.title('Top TF-IDF Terms')
plt.show()

# Perform sentiment analysis using VADER
sia = SentimentIntensityAnalyzer()
global_tfidf_df['Sentiment Score'] = global_tfidf_df['Term'].apply(lambda term: sia.polarity_scores(term)['compound'])
global_tfidf_df['Sentiment-Upvote Score'] = df['upvote_ratio']



# Display the resulting DataFrame
print(global_tfidf_df[['Term', 'TF-IDF Score', 'Sentiment Score', 'Sentiment-Upvote Score']])