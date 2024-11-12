import argparse
import requests

# Define the base URL for the local Flask app
BASE_URL = "http://127.0.0.1:6000"
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400


def handle_response(response, title=None):
    try:
        response.raise_for_status()
        data = response.json()
        if title:
            print("Recommendations for:", data.get("matched_title", title))
            print("Method Used:", data.get("method", "Unknown"))
            print("Recommended Movies:")
            for i, movie in enumerate(data.get("recommendations", []), start=1):
                print(f"{i}. {movie}")
        else:
            print(data)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == HTTP_NOT_FOUND:
            print("Resource not found or invalid input.")
        elif response.status_code == HTTP_BAD_REQUEST:
            print("Bad request. Please check your input parameters.")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        print("Could not connect to the backend. Ensure the Flask app is running on localhost.")


def recommend_movie(title, user_id):
    """Request movie recommendations from the backend for a given title and user ID."""
    url = f"{BASE_URL}/recommend"
    params = {"title": title, "user_id": user_id}
    response = requests.get(url, params=params)
    handle_response(response, title)


def rated_movies_stats(endpoint):
    """Fetch rated movies statistics from the specified endpoint."""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    handle_response(response)


def parse_arguments():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="CLI for Movie Recommendation System")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--least-rated", action="store_true", help="Get the least rated movies")
    group.add_argument("--most-rated", action="store_true", help="Get the most rated movies")
    parser.add_argument("title", nargs="?", type=str, help="Title of the movie to get recommendations for")
    parser.add_argument("user_id", nargs="?", type=int, help="User ID for personalized recommendations")
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.least_rated:
        rated_movies_stats("least_rated_movies")
    elif args.most_rated:
        rated_movies_stats("most_rated_movies")
    else:
        if args.title and args.user_id is not None:
            recommend_movie(args.title, args.user_id)
        else:
            print("Error: 'title' and 'user_id' are required for movie recommendations.")
            argparse.ArgumentParser(description="CLI for Movie Recommendation System").print_help()


if __name__ == "__main__":
    main()