from flask import Flask, jsonify, request

from machine_learning.engine import MovieRecommendationEngine

app = Flask(__name__)

# Initialize the recommendation engine
recommendation_engine = MovieRecommendationEngine()

# Constants
TITLE_ERROR = {"error": "Title parameter is required"}
USER_ID_ERROR = {"error": "User ID parameter is required and should be an integer"}
USER_ID_NOT_FOUND_ERROR = {"error": "User ID not found"}
MOVIE_NOT_FOUND_ERROR_TEMPLATE = "Movie title '{}' not found"


def validate_inputs(title, user_id):
    """Validate the title and user_id inputs."""
    if not title:
        return TITLE_ERROR, 400
    if user_id is None:
        return USER_ID_ERROR, 400
    return None, None


def handle_errors(method, title):
    """Handle specific error cases with appropriate status codes."""
    if method == "User ID not found":
        return USER_ID_NOT_FOUND_ERROR, 404
    if method == "Movie title not found":
        return {"error": MOVIE_NOT_FOUND_ERROR_TEMPLATE.format(title)}, 404
    return None, None


@app.route('/recommend', methods=['GET'])
def recommend_movies():
    """Endpoint for recommending movies."""
    title = request.args.get('title')
    user_id = request.args.get('user_id', type=int)

    # Validate inputs
    error_response, status_code = validate_inputs(title, user_id)
    if error_response:
        return jsonify(error_response), status_code

    # Get recommendations
    recommendations, method, matched_title = recommendation_engine.recommend_movies(title=title, user_id=user_id)

    # Handle errors
    error_response, status_code = handle_errors(method, title)
    if error_response:
        return jsonify(error_response), status_code

    # Successful response
    return jsonify({
        "method": method,
        "matched_title": matched_title,
        "recommendations": recommendations
    }), 200


@app.route('/least_rated_movies', methods=['GET'])
def get_least_rated_movies():
    """Endpoint for getting the least rated movies."""
    return jsonify(recommendation_engine.least_rated_movies.to_dict()), 200


@app.route('/most_rated_movies', methods=['GET'])
def get_most_rated_movies():
    """Endpoint for getting the most rated movies."""
    return jsonify(recommendation_engine.most_rated_movies.to_dict()), 200


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6000)
