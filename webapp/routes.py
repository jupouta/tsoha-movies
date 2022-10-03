from flask import current_app as app
from flask import render_template, request, redirect, session

from .actions import Actions
actions = Actions()

@app.route("/")
def index():
    movies = actions.get_movies()
    return render_template("index.html", movies=movies)

@app.route('/login', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        user=request.form['user']
        password=request.form['password']

        result = actions.check_user(user)
        if not result:  # invalid user
            return render_template('error.html', error_message='Käyttäjää ei löytynyt')
        else:
            user_password = result.password
            if actions.check_password_in_hash(user_password, password):
                session['user'] = result.id
                session['username'] = result.username
                return redirect('/')
            else:
                return render_template('error.html', error_message='Väärä käyttäjätunnus tai salasana')

    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['user']
        password = request.form['password']
        password_again = request.form['password2']

        if not actions.check_user(username):
            if password != password_again:
                return render_template('error.html', error_message='Salasanat eroavat. Tarkista molemmat salasanat.')
            else:
                actions.add_new_user(username, password)
                return redirect('/')
        else:
            return render_template('error.html', error_message='Käyttäjä löytyy jo. Valitse uusi käyttäjätunnus.')

@app.route('/movies')
def query():
    if 'query' in request.args:
        query = request.args['query']
        movies = actions.find_movies_by_name(query)
        return render_template('movies.html', movies=movies)
    else:
        movies = actions.get_movies()
        return render_template('movies.html', movies=movies)

@app.route('/movies/<int:id>', methods=['GET', 'POST'])
def movie(id):
    if request.method == 'POST':
        stars = request.form.get('stars')
        review = request.form.get('review')
        try:
            actions.give_review(stars, review, id, session['user'])
        except:
            return render_template('error.html', error_message='Et ole kirjautunut')

    movie = actions.find_movie_by_id(id)
    reviews = actions.get_reviews_for_movie(id)
    return render_template('movie.html',
                           movie=movie,
                           reviews=reviews)

@app.route("/test")
def test():
    return "Hello world"
