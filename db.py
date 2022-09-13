from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

db = SQLAlchemy(app)


app.secret_key = getenv("SECRET_KEY")