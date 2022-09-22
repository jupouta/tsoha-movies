DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS stars;
DROP TABLE IF EXISTS reviews;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    year INTEGER,
    director TEXT,
    description TEXT
);

CREATE TABLE stars (
    id SERIAL PRIMARY KEY,
    stars INTEGER,
    user_id INTEGER REFERENCES users,
    movie_id INTEGER REFERENCES movies
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    movie_id INTEGER REFERENCES movies,
    star_id INTEGER REFERENCES stars,
    comment TEXT
);
