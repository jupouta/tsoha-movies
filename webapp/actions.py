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
        return result

    def check_password_in_hash(self, user_password, given_password):
        return check_password_hash(user_password, given_password)

    def get_movies(self):
        result = self.database.get_movies()
        if not result:
            result = self.database.get_movies_without_stars()
        return result

    def get_movie_names(self):
        result = [movie.name for movie in self.database.get_movie_names()]
        return result

    def find_movies_by_name(self, name):
        return self.database.find_movies_by_name(name.lower())

    def find_movie_by_id(self, id):
        result = self.database.find_movie_by_id(id)
        if not result:
            result = self.database.find_movie_by_id_without_stars(id)
        return result

    def give_star_review(self, user, stars, movie_id):
        if self.database.get_star_review_by_user(user, movie_id):
            star_id = self.database.update_star_review_by_user(user, movie_id, stars)
        else:
            star_id = self.database.add_new_star_review(user, int(stars), movie_id)
        return star_id

    def give_review(self, stars, review, movie_id, user_id):
        star_id = self.give_star_review(user_id, stars, movie_id)

        # TODO: mitä jos sama käyttäjä lisää kommentin?
        if review != '':
            self.database.add_new_review(user_id, star_id, review, movie_id)

    # TODO: delete?
    def get_stars_for_movie(self, movie_id):
        result = self.database.get_stars_for_movie(movie_id)
        print(result)
        return result[0]

    # TODO: delete?
    def get_star_count_for_movie(self, movie_id):
        result = self.database.get_star_count_for_movie(movie_id)
        return result['count']

    def get_reviews_for_movie(self, movie_id):
        result = self.database.get_reviews_for_movie(movie_id)
        return result

    def make_request(self, request_txt, movie_id, user_id):
        self.database.make_request_for_movie(request_txt, movie_id, user_id)

    def get_requests_for_movie(self, movie_id):
        result = self.database.get_requests_for_movie(movie_id)
        return result
