import pandas as pd
from fuzzywuzzy import process

from machine_learning.collaborative_filtering import CollaborativeFilteringEngine
from machine_learning.content_filtering import ContentFilteringEngine


class MovieRecommendationEngine:
    RATINGS_PATH = './data/raw/ratings.csv'
    MOVIES_PATH = './data/raw/movies.csv'

    def __init__(self, ratings_path=RATINGS_PATH, movies_path=MOVIES_PATH, min_ratings_threshold=5):
        self.ratings_path = ratings_path
        self.movies_path = movies_path
        self.min_ratings_threshold = max(min_ratings_threshold, 5)
        self._load_data()

    def _load_data(self):
        self.ratings_data = pd.read_csv(self.ratings_path)
        self.movies_data = pd.read_csv(self.movies_path)
        self.collaborative_filtering = CollaborativeFilteringEngine(self.ratings_data)
        self.content_filtering = ContentFilteringEngine(self.movies_data)
        self.merged_ratings = self.ratings_data.merge(self.movies_data, on='movieId')
        self.movie_titles = dict(zip(self.movies_data['movieId'], self.movies_data['title']))

    @property
    def most_rated_movies(self):
        return self.merged_ratings['title'].value_counts().head(10)

    @property
    def least_rated_movies(self):
        return self.merged_ratings['title'].value_counts(ascending=True).head(10)

    def _is_collaborative_applicable(self, movie_id):
        """Checks if collaborative filtering is appropriate based on the movie's rating count."""
        return (movie_index := self.collaborative_filtering.movie_index_map.get(movie_id)) is not None \
            and self.collaborative_filtering.movie_ratings_count[movie_index] >= self.min_ratings_threshold

    def _validate_user_id(self, user_id):
        """Validates if the user ID exists in the ratings data."""
        return user_id in self.ratings_data['userId'].values

    def _find_movie_id(self, title):
        """Finds the closest matching movie ID for a given title."""
        matched_title = process.extractOne(title, self.movies_data['title'])
        if matched_title:
            movie_id = self.movies_data.loc[self.movies_data['title'] == matched_title[0], 'movieId'].iloc[0]
            return movie_id, matched_title[0]
        return None, None

    def recommend_movies(self, title, user_id, num_recommendations=5):
        """Recommends similar movies, selecting the appropriate method and validating input."""
        if not self._validate_user_id(user_id):
            return [], "User ID not found", None

        movie_id, matched_title = self._find_movie_id(title)
        if not movie_id:
            return [], "Movie title not found", None

        if self._is_collaborative_applicable(movie_id):
            similar_movie_ids = self.collaborative_filtering.get_similar_movies(movie_id, num_recommendations)
            recommendations = [self.movie_titles[id_] for id_ in similar_movie_ids]
            method_used = "Collaborative Filtering"
        else:
            recommendations = self.content_filtering.get_similar_movies(title, num_recommendations)
            method_used = "Content Filtering"

        return recommendations, method_used, matched_title

    def show_statistics(self, show_plot=False):
        """Displays statistics using utils and engines."""
        print("Collaborative Filtering Statistics:")
        print(self.collaborative_filtering.get_statistics())
        print(f"Sparsity Rate: {self.collaborative_filtering.get_sparsity():.2f}")

        if show_plot:
            self.collaborative_filtering.plot_ratings_distribution()
            self.collaborative_filtering.plot_ratings_density()
            self.content_filtering.plot_genre_frequencies()
