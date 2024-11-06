import argparse
import requests

# Define the base URL for the local Flask app
BASE_URL = "http://127.0.0.1:6000"


def recommend_movie(title, user_id):
    """Request movie recommendations from the backend for a given title and user ID."""
    url = f"{BASE_URL}/recommend"
    params = {"title": title, "user_id": user_id}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for 4xx/5xx responses

        data = response.json()
        print("Recommendations for:", data.get("matched_title", title))
        print("Method Used:", data.get("method", "Unknown"))
        print("Recommended Movies:")
        for i, movie in enumerate(data.get("recommendations", []), start=1):
            print(f"{i}. {movie}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 404:
            print("Resource not found or invalid input.")
        elif response.status_code == 400:
            print("Bad request. Please check your input parameters.")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        print("Could not connect to the backend. Ensure the Flask app is running on localhost.")


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="CLI for Movie Recommendation System")
    parser.add_argument("title", type=str, help="Title of the movie to get recommendations for")
    parser.add_argument("user_id", type=int, help="User ID for personalized recommendations")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to recommend movies
    recommend_movie(args.title, args.user_id)


if __name__ == "__main__":
    main()
