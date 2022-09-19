from flask import current_app as app
from flask import render_template, request, redirect, session

from .actions import Actions
actions = Actions()

@app.route("/")
def index():
    movies = actions.get_movie_names()
    return render_template("index.html", movies=movies)

@app.route("/login", methods=["POST"])
def result():
    user=request.form["user"]
    password=request.form["password"]

    session["user"] = user
    return redirect("/")

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')

@app.route('/movies')
def query():
    if 'query' in request.args:
        query = request.args['query']
        movies = actions.find_movies_by_name(query)
        return render_template('movies.html', movies=movies)
    else:
        movies = actions.get_movies()
        return render_template('movies.html', movies=movies)

@app.route('/movies/<int:id>')
def movie(id):
    movie = actions.find_movie_by_id(id)
    return render_template('movie.html', movie=movie)

@app.route("/test")
def test():
    return "Hello world"