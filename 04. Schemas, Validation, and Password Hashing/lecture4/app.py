"""
Lecture 4 application to learn:

* Schemas
* User sign-ups
* Password hashing
"""

import enum
import os
import re

from flask import (
    Flask,
    request,
)
from flask_restful import (
    Api,
    Resource,
)
from hashlib import scrypt

from lecture4.models import *

URL = "postgresql://{user}:{password}@{server}:{port}/{database}".format(
    user = os.environ["USER"],
    password = os.environ["PASSWORD"],
    server = os.environ["SERVER"],
    port = os.environ["PORT"],
    database = os.environ["DATABASE"],
)

app = Flask(__name__)
api = Api(app)
engine = db.create_engine(URL)

class UserResource(Resource):
    def get(self, user_id = None):
        allowed_keys = {"user_id", "username", "first_name", "last_name"}
        with Session(engine) as con:
            #   Get info on the current user when it is defined
            if user_id is not None:
                user = con.get(User, user_id)
                result = {"data": {"user": [{
                    key: value for key, value in user.__dict__.items() if key in allowed_keys
                }]}}
                return result

            if request.path.endswith("/users/"):
                #   Get all users when no user_id is defined
                all_users = con.query(User).all()
                result = {"data": {"users": [
                    {key: value for key, value in user.__dict__.items() if key in allowed_keys} \
                    for user in all_users
                    ]}}
                return result

            return 400

    def post(self):
        #   Create a new user
        data = request.json
        if not "username" in data and "password" in data:
            return "Must provide username and password", 400

        #   Validate password
        raw_password = str(data["password"])
        if not self.validate_password(raw_password):
            return "Bad password", 400

        #   Store password hash and salt
        salt = os.urandom(16)
        password = scrypt(
            password = raw_password.encode(), salt = salt,
            n = 2**10, r = 8, p = 1
            #   https://words.filippo.io/the-scrypt-parameters/
        )
        data["password_hash"] = password
        data["password_salt"] = salt
        del data["password"]

        user = User(**data)

        with Session(engine) as con:
            con.add(user)
            con.commit()
            return 201

    @staticmethod
    def validate_password(password):
        ok = True
        ok = ok and bool(re.search("[A-Z]", password))
        ok = ok and bool(re.search("\W", password))
        ok = ok and bool(re.search("[0-9]", password))
        return ok


api.add_resource(
    UserResource,
    "/user/<int:user_id>",
    "/users/",
    "/signup/",
)

