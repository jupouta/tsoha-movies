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

    result = actions.check_user(user)
    if not result:  # invalid user
        # TODO: ilmoitus
        return redirect("/")
    else:
        user_password = result.password
        if actions.check_password_in_hash(user_password, password):
            session["user"] = result.id
            # TODO: tallenna myös käyttäjänimi html:ää varten
            return redirect("/")
        else:
            # TODO: ilmoitus
            return redirect("/")

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['user']
        password = request.form['password']
        password_again = request.form['password2']
        # TODO: check passwords are the same
        actions.add_new_user(username, password)

        return redirect("/")

@app.route('/movies')
def query():
    if 'query' in request.args:
        query = request.args['query']
        movies = actions.find_movies_by_name(query)
        return render_template('movies.html', movies=movies)
    else:
        movies = actions.get_movies()
        return render_template('movies.html', movies=movies)

@app.route('/movies/<int:id>', methods=["GET", "POST"])
def movie(id):
    if request.method == 'POST':
        stars = request.form.get('stars')
        try:
            print(session['user'], id)
            # TODO: ylikirjoita(?), jos sama käyttäjä arvioi uudelleen
            actions.give_star_review(session['user'], stars, id)
        except:
            # TODO: handle error
            print('user not found')

    movie = actions.find_movie_by_id(id)
    all_stars = actions.get_stars_for_movie(id)
    return render_template('movie.html', movie=movie, stars=all_stars)

@app.route("/test")
def test():
    return "Hello world"
