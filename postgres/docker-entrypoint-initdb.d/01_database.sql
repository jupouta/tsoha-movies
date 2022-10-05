DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS stars CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS requests CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
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
    comment TEXT,
    posted_at TIMESTAMP
);

CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    movie_id INTEGER REFERENCES movies,
    request TEXT,
    posted_at TIMESTAMP
);
