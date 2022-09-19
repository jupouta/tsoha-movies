

class Database:

    def __init__(self, db):
        self.db = db
        self.db.session.execute('SELECT 1')

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

