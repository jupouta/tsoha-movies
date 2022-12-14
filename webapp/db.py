
class Database:

    def __init__(self, db):
        self.db = db

    def get_user(self, username):
        result = self.db.session.execute('SELECT password, id, username, role \
            FROM users \
            WHERE username=:username;',
            {'username':username})
        user = result.fetchone()
        return user

    def add_new_user(self, username, password):
        self.db.session.execute('INSERT INTO users (username, password) \
            VALUES (:username, :password)',
            {'username':username, 'password':password})
        self.db.session.commit()

    def get_movies(self):
        result = self.db.session.execute('SELECT m.*, ROUND(AVG(s.stars), 2) AS star_avg \
            FROM movies AS m \
            LEFT JOIN stars AS s ON m.id=s.movie_id \
            GROUP BY m.id, m.name, m.year, m.director, m.description;')
        movies = result.fetchall()
        return movies

    def get_movies_in_order(self):
        result = self.db.session.execute('SELECT m.*, ROUND(AVG(s.stars), 2) AS star_avg \
            FROM movies AS m \
            LEFT JOIN stars AS s ON m.id=s.movie_id \
            GROUP BY m.id, m.name, m.year, m.director, m.description \
            ORDER BY star_avg DESC NULLS LAST LIMIT 20;')
        movies = result.fetchall()
        return movies

    def find_movies_by_name(self, name):
        result = self.db.session.execute('SELECT * FROM movies \
            WHERE LOWER(name) LIKE :name;', {'name':'%'+name+'%'})
        movies = result.fetchall()
        return movies

    def find_movie_by_id(self, movie_id):
        result = self.db.session.execute('SELECT m.*, ROUND(AVG(s.stars), 2) AS star_avg,\
            COUNT(s.stars) as star_count \
            FROM movies AS m LEFT JOIN stars AS s ON m.id=s.movie_id \
            WHERE m.id=:movie_id GROUP BY m.id;',
            {'movie_id':movie_id})
        movie = result.fetchone()
        return movie

    def add_new_movie(self, name, director, year, description):
        result = self.db.session.execute('INSERT INTO movies (name, director, year, description) \
            VALUES (:name, :director, :year, :description) \
            RETURNING id',
            {'name':name, 'director':director, 'year':year, 'description':description})
        star_id = result.fetchone()[0]
        self.db.session.commit()
        return star_id

    def delete_movie(self, movie_id):
        result = self.db.session.execute('DELETE FROM movies WHERE id=:movie_id;',
                                {'movie_id': movie_id})
        self.db.session.commit()
        return result

    def add_new_star_review(self, user_id, stars, movie_id):
        result = self.db.session.execute('INSERT INTO stars (user_id, stars, movie_id) \
            VALUES (:user_id, :stars, :movie_id) RETURNING id',
            {'user_id':user_id, 'stars':stars, 'movie_id':movie_id})
        star_id = result.fetchone()[0]
        self.db.session.commit()
        return star_id

    def get_star_review_by_user(self, user, movie_id):
        result = self.db.session.execute('SELECT stars FROM stars \
            WHERE movie_id=:movie_id AND user_id=:user_id;',
            {'movie_id':movie_id, 'user_id':user})
        star = result.fetchone()
        return star

    def update_star_review_by_user(self, user, movie_id, stars):
        result = self.db.session.execute('UPDATE stars SET stars=:stars \
            WHERE user_id=:user_id AND movie_id=:movie_id RETURNING id',
            {'stars':stars, 'user_id':user, 'movie_id':movie_id})
        star_id = result.fetchone()[0]
        self.db.session.commit()
        return star_id

    def add_new_review(self, user_id, star_id, review, movie_id):
        self.db.session.execute('INSERT INTO reviews \
            (user_id, movie_id, star_id, comment, posted_at) \
            VALUES (:user_id, :movie_id, :star_id, :comment, NOW())',
            {'user_id':user_id, 'movie_id':movie_id, 'star_id':star_id, 'comment':review})
        self.db.session.commit()

    def get_reviews_for_movie(self, movie_id):
        result = self.db.session.execute('SELECT r.id, r.comment, \
            TO_CHAR(r.posted_at, \'DD/MM/YY HH:MI\') as posted_at, \
            u.username FROM reviews r, users u WHERE movie_id=:movie_id AND r.user_id=u.id',
            {'movie_id':movie_id})
        reviews = result.fetchall()
        return reviews

    def make_request_for_movie(self, request_txt, movie_id, user_id):
        self.db.session.execute('INSERT INTO requests (user_id, movie_id, request, posted_at) \
            VALUES (:user_id, :movie_id, :request, NOW())',
            {'user_id':user_id, 'movie_id':movie_id, 'request':request_txt})
        self.db.session.commit()

    def get_requests_for_movie(self, movie_id):
        result = self.db.session.execute('SELECT r.request, \
            TO_CHAR(r.posted_at, \'DD/MM/YY HH:MI\') as posted_at, \
            u.username FROM requests r, users u WHERE movie_id=:movie_id AND r.user_id=u.id',
            {'movie_id':movie_id})
        requests = result.fetchall()
        return requests

    def update_movie_info(self, name, director, year, description, movie_id):
        result = self.db.session.execute('UPDATE movies \
            SET name=:name, director=:director, year=:year, description=:description \
            WHERE id=:movie_id RETURNING id',
            {'name':name, 'director':director,
             'year':year, 'description':description,
             'movie_id':movie_id})

        star_id = result.fetchone()[0]
        self.db.session.commit()
        return star_id

    def delete_review_for_movie(self, review_id):
        result = self.db.session.execute('DELETE FROM reviews WHERE id=:review_id;',
                                {'review_id': review_id})
        self.db.session.commit()
        return result
