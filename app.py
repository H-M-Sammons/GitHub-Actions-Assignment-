import os

from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, request

from src.models import db
from src.repositories.movie_repository import movie_repository_singleton

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/movies')
def list_all_movies():
    all_movies = movie_repository_singleton.get_all_movies()
    return render_template('list_all_movies.html', list_movies_active=True, movies=all_movies)


@app.get('/movies/<int:movie_id>')
def get_single_movie(movie_id: int):
    single_movie = movie_repository_singleton.get_movie_by_id(movie_id)
    return render_template('get_single_movie.html', movie=single_movie)


@app.get('/movies/new')
def create_movies_form():
    return render_template('create_movies_form.html', create_rating_active=True)


@app.post('/movies')
def create_movie():
    title = request.form.get('title', '')
    director = request.form.get('director', '')
    rating = request.form.get('rating', 0, type=int)
    if title == '' or director == '' or rating < 1 or rating > 5:
        abort(400)
    created_movie = movie_repository_singleton.create_movie(title, director, rating)
    return redirect(f'/movies/{created_movie.movie_id}')


@app.get('/movies/search')
def search_movies():
    found_movies = []
    q = request.args.get('q', '')
    if q != '':
        found_movies = movie_repository_singleton.search_movies(q)
    return render_template('search_movies.html', search_active=True, movies=found_movies, search_query=q)
