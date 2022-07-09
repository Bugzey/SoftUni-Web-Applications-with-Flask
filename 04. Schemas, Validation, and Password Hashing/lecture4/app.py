"""
Lecture 4 application to learn:

* Schemas
* User sign-ups
* Password hashing
"""

import enum
from hashlib import scrypt
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
from marshmallow import (
    Schema,
    fields,
    ValidationError,
    validate,
)

#   Optional modules; not used
#   from password_strength import PasswordPolicy
#   import phone_numbers

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


#   TODO: decorator that wraps resource post methods and validates a schema given as an argument to
#   the decorator

#   Schemas
class BaseUserSchema(Schema):
    username = fields.String(required = True)
    email = fields.Email(required = True)
    first_name = fields.String(required = True)
    last_name = fields.String(required = True)
    phone = fields.String()


def validate_password(password):
    ok = True
    ok = ok and bool(re.search("[A-Z]", password))
    ok = ok and bool(re.search("\W", password))
    ok = ok and bool(re.search("[0-9]", password))

    if not ok:
        raise ValidationError("Invalid password")

class UserSignUpSchema(BaseUserSchema):
    password = fields.String(
        required = True, validate = [validate_password, validate.Length(min = 8)]
    )

    #   method way to validate data
    #   marshmallow.validates("email")
    #   def validate_password(self, password):
    #       pass


#   API resources
class UserSignUpResource(Resource):
    def post(self):
        data = request.json
        schema = UserSignUpSchema()
        errors = schema.validate(data)

        if errors:
            return errors

        password_hash, salt = self.generate_password_hash_and_salt(data["password"])
        data["password_hash"] = password_hash
        data["password_salt"] = salt
        del data["password"]

        user = User(**data)
        with Session(engine) as con:
            con.add(user)
            con.commit()

    @staticmethod
    def generate_password_hash_and_salt(password: str) -> tuple[bytes, bytes]:
        #   Store password hash and salt
        salt = os.urandom(16)
        password_hash = scrypt(
            password = password.encode(), salt = salt,
            n = 2**10, r = 8, p = 1
            #   https://words.filippo.io/the-scrypt-parameters/
        )
        return password_hash, salt


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

    def legacy_post(self):
        #   Saved for reference - wrote this before using schemas
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
)
api.add_resource(UserSignUpResource, "/signup/")
