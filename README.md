# 🎬 Yasmeen's CineMatch

A content-based movie recommender system. Type a movie you like and get 6 similar movies, each with a match percentage.

## How it works
- Combines each movie's overview, genres, keywords, top 3 actors and director into "tags"
- Converts the tags to numbers with TF-IDF (written in pure Python)
- Finds the closest movies using cosine similarity

## Tech stack
Python, Flask, HTML/CSS, Gunicorn, Render

## Dataset
TMDB 5000 Movie Dataset (Kaggle)

## Run locally
    pip install flask
    python build_tags.py
    python app.py

Then open [http://127.0.0.1:5000](https://movie-recommender-ser4mkkxjtezyk9jp8zo6a.streamlit.app/)

## Author
Yasmeen Khan
