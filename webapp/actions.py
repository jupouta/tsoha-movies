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
        return result

    def get_movies_in_order(self):
        result = self.database.get_movies_in_order()
        return result

    def find_movies_by_name(self, name):
        return self.database.find_movies_by_name(name.lower())

    def find_movie_by_id(self, movie_id):
        result = self.database.find_movie_by_id(movie_id)
        return result

    def add_new_movie(self, name, director, year, description):
        movie_id = self.database.add_new_movie(name, director, year, description)
        return movie_id

    def delete_movie(self, movie_id):
        return self.database.delete_movie(movie_id)

    def give_star_review(self, user, stars, movie_id):
        if self.database.get_star_review_by_user(user, movie_id):
            star_id = self.database.update_star_review_by_user(user, movie_id, stars)
        else:
            star_id = self.database.add_new_star_review(user, int(stars), movie_id)
        return star_id

    def give_review(self, stars, review, movie_id, user_id):
        star_id = self.give_star_review(user_id, stars, movie_id)
        self.database.add_new_review(user_id, star_id, review, movie_id)

    def get_reviews_for_movie(self, movie_id):
        result = self.database.get_reviews_for_movie(movie_id)
        return result

    def make_request(self, request_txt, movie_id, user_id):
        self.database.make_request_for_movie(request_txt, movie_id, user_id)

    def get_requests_for_movie(self, movie_id):
        result = self.database.get_requests_for_movie(movie_id)
        return result

    def update_movie_info(self, name, director, year, description, movie_id):
        self.database.update_movie_info(name, director, year, description, movie_id)

    def delete_review_for_movie(self, review_id):
        return self.database.delete_review_for_movie(review_id)

    def check_csrf_token(self, csrf_token, validate_token):
        return csrf_token == validate_token

    def check_user_role(self, user_role):
        return user_role == 1
