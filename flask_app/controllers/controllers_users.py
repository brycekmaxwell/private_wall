from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models import model_messages
from flask_app.models import models_users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def home():
    return render_template("log_in.html")

@app.route("/register", methods=["POST"])
def register():
    valid_user = models_users.User.create_valid_user(request.form)
    if not valid_user:
        return redirect("/")
    session["user_id"] = valid_user.id
    return redirect("/dashboard")

@app.route("/log_in", methods=["POST"])
def login():
    valid_user = models_users.User.authenticated_user_by_input(request.form)
    if not valid_user:
        flash("Invalid Email","login")
        return redirect("/")
    if not bcrypt.check_password_hash(models_users.password, request.form["password"]):
        flash("Invalid Password", "login")
        return redirect("/")
    session["user_id"]=valid_user.id
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session: 
        return redirect("/logout")
    user = models_users.User.get_by_id({"id":session["user_id"]})
    messages = model_messages.Message.get_user_messages({"id":session["user_id"]})
    users = models_users.User.get_all()
    return render_template("wall.html", user=user, users=users, messages=messages)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")