from . import db
from webapp.db import Database



class Actions:

    def __init__(self):
        self.database = Database(db)

    def add_user(self):
        self.database.db.session.execute('SELECT * FROM users;')
        print('yes')
        return True

    # TODO: refactor these
    def get_movie_names(self):
        result = [movie.name for movie in self.database.get_movie_names()]
        return result

    def find_movies_by_name(self, name):
        result = [movie.name for movie in self.database.find_movies_by_name(name)]
        return result

    def find_movie_by_id(self, id):
        result = self.database.find_movie_by_id(id)
        return result