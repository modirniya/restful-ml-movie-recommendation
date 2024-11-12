import copy
from collections import Counter

from fuzzywuzzy import process
from sklearn.metrics.pairwise import cosine_similarity

from machine_learning.utils import plot_genre_frequencies


class ContentFilteringEngine:
    """
    Class for content-based filtering of movies.
    """
    METADATA_COLUMNS = ['movieId', 'title', 'genres']

    def __init__(self, movies_df):
        self.movies_df = copy.copy(movies_df)
        self._split_genres()
        self.genre_matrix = None
        self.movie_title_to_index = None
        self.similarity_matrix = None
        self.genre_counts = None
        self._initialize_genre_columns()
        self._initialize_similarity_matrix()

    def _split_genres(self):
        self.movies_df['genres'] = self.movies_df['genres'].apply(lambda x: x.split("|"))

    def _initialize_genre_columns(self):
        """Initializes unique genre columns in the movies dataframe."""
        self.genre_counts = Counter(
            genre for genres in self.movies_df['genres'] for genre in genres
        )
        for genre in self.genre_counts:
            self.movies_df[genre] = self.movies_df['genres'].apply(lambda genres: int(genre in genres))

    def _initialize_similarity_matrix(self):
        """Creates a binary genre matrix and computes cosine similarity."""
        self.genre_matrix = self.movies_df.drop(columns=self.METADATA_COLUMNS)
        self.similarity_matrix = cosine_similarity(self.genre_matrix)
        self.movie_title_to_index = {title: idx for idx, title in enumerate(self.movies_df['title'])}

    def get_similar_movies(self, movie_title, num_recommendations=10):
        """Finds similar movies to the given title using content-based filtering."""
        matched_title = process.extractOne(movie_title, self.movies_df['title'])
        if matched_title is None:
            return []
        movie_index = self.movie_title_to_index[matched_title[0]]
        similarity_scores = list(enumerate(self.similarity_matrix[movie_index]))
        similarity_scores = sorted(similarity_scores[1:], key=lambda x: x[1], reverse=True)[:num_recommendations]
        similar_movie_indices = [idx for idx, _ in similarity_scores]
        return self.movies_df['title'].iloc[similar_movie_indices].tolist()

    def plot_genre_frequencies(self):
        """Plot the frequency of each genre in the dataset."""
        plot_genre_frequencies(self.genre_counts)
