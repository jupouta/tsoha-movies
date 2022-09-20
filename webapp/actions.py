from . import db
from webapp.db import Database
from werkzeug.security import check_password_hash, generate_password_hash



class Actions:

    def __init__(self):
        self.database = Database(db)

    def add_new_user(self, username, password):
        hash_password = generate_password_hash(password)
        self.database.add_new_user(username, hash_password)

    def check_user(self, username):
        result = self.database.get_user(username)
        print(result)
        return result

    def check_password_in_hash(self, user_password, given_password):
        return check_password_hash(user_password, given_password)

    def get_movies(self):
        result = self.database.get_movies()
        print(result)
        return result

    # TODO: refactor these
    def get_movie_names(self):
        result = [movie.name for movie in self.database.get_movie_names()]
        return result

    def find_movies_by_name(self, name):
        return self.database.find_movies_by_name(name)

    def find_movie_by_id(self, id):
        result = self.database.find_movie_by_id(id)
        return result

    def give_star_review(self, user, stars, id):
        result = self.database.add_new_star_review(user, int(stars), id)
        print(result)

    def get_stars_for_movie(self, movie_id):
        result = self.database.get_stars_for_movie(movie_id)
        print(result)
        return result[0]
