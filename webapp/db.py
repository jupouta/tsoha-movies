

class Database:

    def __init__(self, db):
        self.db = db

    def get_user(self, username):
        result = self.db.session.execute('SELECT password, id FROM users WHERE username=:username;',
                                         {'username':username})
        user = result.fetchone()
        return user

    def add_new_user(self, username, password):
        self.db.session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                                         {'username':username, 'password':password})
        self.db.session.commit()

    def get_movies(self):
        result = self.db.session.execute('SELECT * FROM movies;')
        movies = result.fetchall()
        return movies

    # TODO: refactor these
    def get_movie_names(self):
        result = self.db.session.execute('SELECT name FROM movies;')
        movies = result.fetchall()
        return movies

    def find_movies_by_name(self, name):
        result = self.db.session.execute('SELECT * FROM movies WHERE name LIKE :name;', {'name':'%'+name+'%'})
        movies = result.fetchall()
        return movies

    def find_movie_by_id(self, id):
        result = self.db.session.execute('SELECT * FROM movies WHERE id=:id;', {'id':id})
        movie = result.fetchone()
        return movie

    def add_new_star_review(self, user_id, stars, movie_id):
        self.db.session.execute('INSERT INTO stars (user_id, stars, movie_id) VALUES (:user_id, :stars, :movie_id)',
                                         {'user_id':user_id, 'stars':stars, 'movie_id':movie_id})
        self.db.session.commit()

    def get_stars_for_movie(self, movie_id):
        result = self.db.session.execute('SELECT ROUND(AVG(stars), 2) FROM STARS WHERE movie_id=:movie_id;', {'movie_id':movie_id})
        stars_avg = result.fetchone()
        return stars_avg


