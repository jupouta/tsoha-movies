from app import app
import actions
from flask import render_template, request, redirect, session


@app.route("/")
def index():
    return render_template("index.html", movies=["Batman", "Casablanca"])

@app.route("/login")
def form():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def result():
    user=request.form["user"]
    password=request.form["password"]

    session["user"] = user
    return redirect("/")