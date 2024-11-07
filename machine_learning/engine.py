import pandas as pd

from machine_learning.collaborative_filtering import CollaborativeFilteringEngine
from machine_learning.content_filtering import ContentFilteringEngine

from fuzzywuzzy import process


class MovieRecommendationEngine:
    def __init__(self, ratings_path, movies_path, min_ratings_threshold=5):
        print("Initializing MovieRecommendationEngine...")

        # Validate min_ratings_threshold
        if min_ratings_threshold < 5:
            print("Warning: min_ratings_threshold cannot be less than 5. Setting it to 5.")
            min_ratings_threshold = 5
        requirements = ""

        self.min_ratings_threshold = min_ratings_threshold
        self.ratings_data = pd.read_csv(ratings_path)
        self.movies_data = pd.read_csv(movies_path)
        self.collaborative_filtering = CollaborativeFilteringEngine(self.ratings_data)
        self.content_filtering = ContentFilteringEngine(self.movies_data)
        self.movie_titles = dict(zip(self.movies_data['movieId'], self.movies_data['title']))

    def _is_collaborative_applicable(self, movie_id):
        """Checks if collaborative filtering is appropriate based on the movie's rating count."""
        movie_index = self.collaborative_filtering.movie_index_map.get(movie_id)
        return movie_index is not None and self.collaborative_filtering.movie_ratings_count[
            movie_index] >= self.min_ratings_threshold

    def _validate_user_id(self, user_id):
        """Validates if the user ID exists in the ratings data."""
        if user_id not in self.ratings_data['userId'].values:
            return False
        return True

    def _find_movie_id(self, title):
        """Finds the closest matching movie ID for a given title."""
        matched_title = process.extractOne(title, self.movies_data['title'])
        if matched_title:
            movie_id = self.movies_data.loc[self.movies_data['title'] == matched_title[0], 'movieId'].iloc[0]
            return movie_id, matched_title[0]
        return None, None

    def recommend_movies(self, title, user_id, num_recommendations=5):
        """Recommends similar movies, selecting the appropriate method and validating input."""

        # Validate user existence
        if not self._validate_user_id(user_id):
            return [], "User ID not found", None

        # Find movie ID and matched title
        movie_id, matched_title = self._find_movie_id(title)
        if not movie_id:
            return [], "Movie title not found", None

        # Choose method based on collaborative applicability
        if self._is_collaborative_applicable(movie_id):
            similar_movie_ids = self.collaborative_filtering.get_similar_movies(movie_id, num_recommendations)
            recommendations = [self.movie_titles[id_] for id_ in similar_movie_ids]
            method_used = "Collaborative Filtering"
        else:
            recommendations = self.content_filtering.get_similar_movies(title, num_recommendations)
            method_used = "Content Filtering"

        return recommendations, method_used, matched_title

    def show_statistics(self):
        """Displays statistics using utils and engines."""
        print("Collaborative Filtering Statistics:")
        print(self.collaborative_filtering.get_statistics())
        print(f"Sparsity Rate: {self.collaborative_filtering.get_sparsity():.2f}")
        # self.collaborative_filtering.plot_distributions()
