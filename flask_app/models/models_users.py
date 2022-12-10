from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import model_messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "private_wall"

    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data ["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls,data):
        query = "INSERT into users (first_name, last_name, email, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) <1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) <1:
            return False
        return cls(results[0])

    @classmethod 
    def authenticated_user_by_input(cls, user_input):
        is_valid=True
        existing_user=cls.get_by_email({"email": user_input["email"]})
        password_valid=True
        if not existing_user:
            is_valid=False
        else:
            data = {
                "email": user_input["email"]
            }
            query ="SELECT password FROM users WHERE email = %(email)s;"
            hashed_password =connectToMySQL(cls.DB).query_db(query,data)[0]["password"]
            password_valid = bcrypt.check_password_hash(hashed_password, user_input["password"])
            if not password_valid:
                is_valid=False
        if not is_valid:
            flash("Password and email do not match", "login")
            return False
        return existing_user

    @classmethod
    def create_valid_user(cls, user):
        if not cls.validate(user):
            return False
        password_hash=bcrypt.generate_password_hash(user["password"])
        user=user.copy()
        user["password"]=password_hash
        query="INSERT into users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        new_user_id=connectToMySQL(cls.DB).query_db(query, user)
        new_user = cls.get_by_id({"id":new_user_id})
        return new_user
        
    @staticmethod
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.DB).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid=False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email!", "register")
            is_valid =False
        if len(user["first_name"]) <= 2:
            flash("First name must be at least 2 characters", "register")
            is_valid=False
        if len(user["last_name"]) <= 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid=False
        if len(user["password"])<10:
            flash("Password must be at least 10 characters", "register")
            is_valid=False
        if user["password"] != user["confirm"]:
            flash("Passwords don't match", "register")
        return is_valid