from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from machine_learning.utils import *


class CollaborativeFilteringEngine:
    def __init__(self, ratings_dataframe):
        self.ratings_data = ratings_dataframe
        self.user_index_map = None
        self.movie_index_map = None
        self.index_to_user_map = None
        self.index_to_movie_map = None
        self.user_movie_matrix = None
        self.user_ratings_count = None
        self.movie_ratings_count = None
        self.build_user_movie_matrix()

    def build_user_movie_matrix(self):
        """Creates a sparse matrix for user-item interactions."""
        num_users = self.ratings_data['userId'].nunique()
        num_movies = self.ratings_data['movieId'].nunique()

        self.user_index_map = {user_id: index for index, user_id in enumerate(self.ratings_data['userId'].unique())}
        self.movie_index_map = {movie_id: index for index, movie_id in enumerate(self.ratings_data['movieId'].unique())}
        self.index_to_user_map = {index: user_id for user_id, index in self.user_index_map.items()}
        self.index_to_movie_map = {index: movie_id for movie_id, index in self.movie_index_map.items()}

        user_indices = [self.user_index_map[user_id] for user_id in self.ratings_data['userId']]
        movie_indices = [self.movie_index_map[movie_id] for movie_id in self.ratings_data['movieId']]

        self.user_movie_matrix = csr_matrix((self.ratings_data["rating"], (user_indices, movie_indices)),
                                            shape=(num_users, num_movies))
        self.user_ratings_count = self.user_movie_matrix.getnnz(axis=1)
        self.movie_ratings_count = self.user_movie_matrix.getnnz(axis=0)

    def get_similar_movies(self, movie_id, num_recommendations=5, similarity_metric='cosine'):
        """Finds similar movies to the given movie_id based on collaborative filtering."""
        movie_index = self.movie_index_map.get(movie_id)
        if movie_index is None:
            return []

        knn = NearestNeighbors(n_neighbors=num_recommendations + 1, metric=similarity_metric, algorithm="brute")
        knn.fit(self.user_movie_matrix.T)
        neighbors = knn.kneighbors(self.user_movie_matrix.T[movie_index], return_distance=False).flatten()
        similar_movie_ids = [self.index_to_movie_map[idx] for idx in neighbors[1:]]

        return similar_movie_ids

    def get_sparsity(self):
        """Uses utils to calculate sparsity."""
        return calculate_sparsity(self.user_movie_matrix)

    def get_statistics(self):
        """Uses utils to get basic statistics."""
        return get_rating_statistics(self.user_ratings_count, self.movie_ratings_count)

    def plot_ratings_density(self):
        """Uses utils to plot rating density."""
        plot_ratings_density(self.user_ratings_count, self.movie_ratings_count)

    def plot_ratings_distribution(self):
        """Uses utils to plot rating distributions."""
        plot_ratings_distribution(self.ratings_data)
