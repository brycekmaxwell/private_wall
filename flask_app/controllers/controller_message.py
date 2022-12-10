from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import models_users
from flask_app.models import model_messages

@app.route("/post_message", methods=["POST"])
def post_message():
    if "user_id" not in session:
        return redirect("/")
    model_messages.save(request.form)
    return redirect("/dashboard")

@app.route("/destroy/message/<int:message_id>")
def destroy_message(message_id):
    model_messages.destroy(message_id)
    return redirect("/dashboard")

