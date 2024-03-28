# recommendation.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

class MovieRecommendationEngine:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.features = ['Votes', 'Rating', 'Year']
        self.X = self.df[self.features]
        self.scaler = MinMaxScaler()
        self.X_normalized = self.scaler.fit_transform(self.X)
        self.knn_model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
        self.knn_model.fit(self.X_normalized)

    def get_recommendations(self, user_rating, user_votes, user_year):
        input_data = self.scaler.transform([[user_votes, user_rating, user_year]])
        _, indices = self.knn_model.kneighbors(input_data)
        
        # Select 'Title', 'Rating', 'Year', and 'Description' columns and limit to 5 rows
        recommended_movies = self.df.iloc[indices[0]][['Title', 'Rating', 'Year', 'Description']].head(5)
        
        return recommended_movies
