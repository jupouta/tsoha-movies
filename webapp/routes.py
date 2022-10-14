import os

from flask import current_app as app
from flask import render_template, request, redirect, session, Response, abort

from .actions import Actions
actions = Actions()

@app.route('/')
def index():
    movies = actions.get_movies()
    return render_template('index.html', movies=movies)

@app.route('/login', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        user=request.form['user']
        password=request.form['password']

        result = actions.check_user(user)
        if not result:  # invalid user
            return render_template('error.html', error_message='Käyttäjää ei löytynyt')

        user_password = result.password
        if actions.check_password_in_hash(user_password, password):
            session['user'] = result.id
            session['username'] = result.username
            session['role'] = result.role
            session['csrf_token'] = os.urandom(16).hex()
            return redirect('/')
        return render_template('error.html', error_message='Väärä käyttäjätunnus tai salasana')

    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['user']
    del session['username']
    del session['role']
    del session['csrf_token']
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['user']
    password = request.form['password']
    password_again = request.form['password2']

    if not actions.check_user(username):
        if password != password_again:
            return render_template('error.html', error_message='Salasanat eroavat. Tarkista molemmat salasanat.')

        actions.add_new_user(username, password)
        return redirect('/')

    return render_template('error.html', error_message='Käyttäjä löytyy jo. Valitse uusi käyttäjätunnus.')

@app.route('/movies')
def query():
    if 'query' in request.args:
        query = request.args['query']
        # TODO: validate query
        if query:
            movies = actions.find_movies_by_name(query)
            return render_template('movies.html', movies=movies)
        else:
            return render_template('error.html', error_message='Haku on viallinen, tarkista muoto')
    else:
        movies = actions.get_movies()
        return render_template('movies.html', movies=movies)

@app.route('/movies/<int:id>', methods=['GET', 'POST'])
def movie(id):
    if request.method == 'POST':
        stars = request.form.get('stars')
        review = request.form.get('review')
        requested = request.form.get('request')
        form_csrf_token = request.form.get('csrf')

        try:
            if not actions.check_csrf_token(session['csrf_token'], form_csrf_token):
                abort(403)
            if stars or review:
                actions.give_review(stars, review, id, session['user'])
            if requested:
                actions.make_request(requested, id, session['user'])
        except:
            return render_template('error.html', error_message='Et ole kirjautunut')
    movie = actions.find_movie_by_id(id)
    if movie:
        # TODO: yhdistä selectit?
        reviews = actions.get_reviews_for_movie(id)
        requests = actions.get_requests_for_movie(id)
        return render_template('movie.html',
                           base_url=request.root_url,
                           movie=movie,
                           reviews=reviews,
                           requests=requests)
    return render_template('error.html', error_message='Tulit virheelliselle sivulle.')

@app.route('/movies/<int:movie_id>/reviews/<int:review_id>', methods=['DELETE'])
def remove_review(movie_id, review_id):
    actions.delete_review_for_movie(review_id)
    return Response('OK', status=302, mimetype='application/json')

    # movie = actions.find_movie_by_id(movie_id)
    # reviews = actions.get_reviews_for_movie(movie_id)
    # requests = actions.get_requests_for_movie(movie_id)
    # return render_template('movie.html',
    #                     base_url=request.root_url,
    #                     movie=movie,
    #                     reviews=reviews,
    #                     requests=requests)

@app.route('/modify/<int:id>', methods=['GET', 'POST'])
def modify_movie(id):
    if request.method == 'POST':
        form_csrf_token = request.form.get('csrf')
        if not actions.check_csrf_token(session['csrf_token'], form_csrf_token):
            abort(403)

        # TODO: validate
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        description = request.form.get('description')
        actions.update_movie_info(name, director, year, description, id)

    movie = actions.find_movie_by_id(id)
    if movie:
        return render_template('modify.html', movie=movie)
    return render_template('error.html', error_message='Tulit virheelliselle sivulle.')

# TODO: delete
@app.route("/test")
def test():
    return "Hello world"
