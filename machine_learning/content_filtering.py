from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process


class ContentFilteringEngine:
    def __init__(self, movies_dataframe):
        self.movies_data = movies_dataframe
        self.genre_matrix = None
        self.movie_index_map = None
        self.cosine_similarity_matrix = None
        self._initialize_genre_matrix()

    def _initialize_genre_matrix(self):
        """Creates a binary genre matrix and computes cosine similarity."""
        unique_genres = set(genre for genres in self.movies_data['genres'].str.split('|') for genre in genres)
        for genre in unique_genres:
            self.movies_data[genre] = self.movies_data['genres'].apply(lambda genres: int(genre in genres))

        self.genre_matrix = self.movies_data.drop(columns=['movieId', 'title', 'genres'])
        self.cosine_similarity_matrix = cosine_similarity(self.genre_matrix)
        self.movie_index_map = {title: idx for idx, title in enumerate(self.movies_data['title'])}

    def get_similar_movies(self, title, num_recommendations=10):
        """Finds similar movies to the given title using content-based filtering."""
        matched_title = process.extractOne(title, self.movies_data['title'])
        if matched_title is None:
            return []

        movie_index = self.movie_index_map[matched_title[0]]
        similarity_scores = list(enumerate(self.cosine_similarity_matrix[movie_index]))
        similarity_scores = sorted(similarity_scores[1:], key=lambda x: x[1], reverse=True)[:num_recommendations]
        similar_movie_indices = [idx for idx, _ in similarity_scores]

        return self.movies_data['title'].iloc[similar_movie_indices].tolist()
