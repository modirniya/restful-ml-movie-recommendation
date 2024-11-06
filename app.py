from flask import Flask, request, jsonify

from machine_learning.engine import MovieRecommendationEngine

app = Flask(__name__)

# Initialize the recommendation engine
ratings_path = './data/raw/ratings.csv'
movies_path = './data/raw/movies.csv'
recommendation_engine = MovieRecommendationEngine(ratings_path=ratings_path, movies_path=movies_path)

@app.route('/recommend', methods=['GET'])
def recommend_movies():
    title = request.args.get('title')
    user_id = request.args.get('user_id', type=int)

    # Validate inputs
    if not title:
        return jsonify({"error": "Title parameter is required"}), 400
    if user_id is None:
        return jsonify({"error": "User ID parameter is required and should be an integer"}), 400

    # Get recommendations
    recommendations, method, matched_title = recommendation_engine.recommend_movies(title=title, user_id=user_id)

    # Handle specific error cases with appropriate status codes
    if method == "User ID not found":
        return jsonify({"error": "User ID not found"}), 404
    if method == "Movie title not found":
        return jsonify({"error": f"Movie title '{title}' not found"}), 404

    # Successful response
    return jsonify({
        "method": method,
        "matched_title": matched_title,
        "recommendations": recommendations
    }), 200

# Run the Flask app on localhost
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6000)
