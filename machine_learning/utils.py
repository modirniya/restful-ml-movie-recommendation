import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def calculate_sparsity(matrix):
    """Calculates the sparsity rate of a given matrix."""
    total_elements = matrix.shape[0] * matrix.shape[1]
    total_ratings = matrix.nnz
    return total_ratings / total_elements


def plot_ratings_density(ratings_per_user, ratings_per_movie):
    """Plots distribution of ratings per user and ratings per movie."""
    plt.figure(figsize=(16, 4))

    # Plot user rating counts
    plt.subplot(1, 2, 1)
    sns.kdeplot(ratings_per_user, fill=True)
    plt.title("Number of Ratings per User")
    plt.xlabel("Ratings per User")
    plt.ylabel("Density")

    # Plot movie rating counts
    plt.subplot(1, 2, 2)
    sns.kdeplot(ratings_per_movie, fill=True)
    plt.title("Number of Ratings per Movie")
    plt.xlabel("Ratings per Movie")
    plt.ylabel("Density")

    plt.show()

def plot_ratings_distribution(ratings):
    sns.countplot(x="rating", data=ratings, palette="viridis")
    plt.title("Distribution of movie ratings", fontsize=14)
    plt.show()

def plot_genre_frequencies(genre_counts):
    genre_frequency_df = pd.DataFrame([genre_counts]).T.reset_index()
    genre_frequency_df.columns = ['genre', 'count']
    sns.barplot(x='genre', y='count', data=genre_frequency_df.sort_values(by='count', ascending=False))
    plt.xticks(rotation=90)
    plt.show()


def get_rating_statistics(ratings_per_user, ratings_per_movie):
    """Returns basic statistics about the number of ratings per user and per movie, with cleaned data types."""
    stats = {
        "Total users": int(len(ratings_per_user)),
        "Most active user ratings": int(ratings_per_user.max()),
        "Least active user ratings": int(ratings_per_user.min()),
        "Total movies": int(len(ratings_per_movie)),
        "Most rated movie": int(ratings_per_movie.max()),
        "Least rated movie": int(ratings_per_movie.min()),
    }
    return stats


