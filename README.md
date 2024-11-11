
# Movie Recommendation CLI & API

This project is a movie recommendation system that provides recommendations via a command-line interface (CLI) and a Flask-based API. Users can get personalized movie recommendations by entering a movie title and their user ID, or they can retrieve lists of the most and least rated movies in the database.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [CLI Commands](#cli-commands)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/movie-recommendation-cli-api.git
   cd movie-recommendation-cli-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask API server:
   ```bash
   flask run --port=6000
   ```
   The API will start at `http://127.0.0.1:6000`.

## Usage

The CLI interacts with the API to provide movie recommendations. Run the CLI using:
```bash
python cli.py [OPTIONS] [TITLE] [USER_ID]
```

### CLI Commands

The CLI accepts three main commands:

1. **Get the least rated movies:**
   ```bash
   python cli.py --least-rated
   ```

2. **Get the most rated movies:**
   ```bash
   python cli.py --most-rated
   ```

3. **Get movie recommendations for a title and user ID:**
   ```bash
   python cli.py "Movie Title" 2
   ```

### API Endpoints

The Flask app provides the following endpoints:

- `GET /recommend`: Returns movie recommendations based on the provided `title` and `user_id` parameters.
  - **Parameters**: `title` (string), `user_id` (integer)
  - **Example**: `http://127.0.0.1:6000/recommend?title=Matrix&user_id=2`

- `GET /least_rated_movies`: Returns a list of the least-rated movies.
  - **Example**: `http://127.0.0.1:6000/least_rated_movies`

- `GET /most_rated_movies`: Returns a list of the most-rated movies.
  - **Example**: `http://127.0.0.1:6000/most_rated_movies`

### Error Handling

The CLI and API handle several types of errors:

- **404**: Resource not found (for example, when an invalid title or user ID is given).
- **400**: Bad request, such as missing or invalid input parameters.
- **500**: Internal server error.

## Project Structure

```
movie-recommendation-cli-api/
├── app.py                # Flask API app
├── cli.py                # Command-line interface
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is open-source and available under the [MIT License](https://mit-license.org/).
