import datetime as dt
from hashlib import scrypt
import os
import re

from flask import request
from flask_restful import Resource
import jwt
from sqlalchemy import (
    select,
)
from sqlalchemy.orm import Session

from lecture5.config import SECRET
from lecture5.models import (
    engine,
    UserModel,
)
from lecture5.schemas import (
    validate_schema,
    UserBaseSchema,
    UserSignUpSchema,
)

class BaseUserResource(Resource):
    @staticmethod
    def generate_token(
        user_id: int,
        valid_time: dt.timedelta = dt.timedelta(days = 1),
    ):
        payload = {
            "sub": user_id,
            "iat": dt.datetime.now(),
            "exp": dt.datetime.now() + valid_time,
        }
        token = jwt.encode(payload, key = SECRET, algorithm = "HS256")
        return token

    @staticmethod
    def validate_token(
        token: str,
    ) -> int:
        try:
            decoded_token = jwt.decode(token, key = SECRET, algorithms = "HS256")
        except jwt.InvalidTokenError:
            return None

        return decoded_token["sub"]


class UserLogInResource(BaseUserResource):
    def post(self):
        username = request.json["username"]
        password = request.json["password"]

        with Session(engine) as sess:
            query = select(UserModel).where(
                (UserModel.username == username) | (UserModel.email == username)
            )
            user = sess.execute(query).scalar()

        if not user:
            return "User not found", 404

        if not self.validate_password(user, password):
            return "Invalid password", 401

        token = self.generate_token(user.id)
        return {"token": token}

    @staticmethod
    def validate_password(user: UserModel, password: str) -> bool:
        salt = user.password_salt
        password_hash = scrypt(
            password = password.encode(), salt = salt,
            n = 2**10, r = 8, p = 1
            #   https://words.filippo.io/the-scrypt-parameters/
        )
        return password_hash == user.password_hash


def login_required(fun):
    def wrapped(*args, **kwargs):
        match = re.search("Bearer (.+)", request.headers["Authorization"])

        if not match:
            return "Missing or invdalid Authorization header", 400

        token = match.group(1)
        user_id = BaseUserResource.validate_token(token)

        if not user_id:
            return "Invalid or expired token", 401

        return fun(*args, **kwargs)

    return wrapped


class UserInfoResource(BaseUserResource):
    @login_required
    def get(self, user_id: int = None):
        with Session(engine) as sess:
            if user_id:
                data = sess.get(UserModel, user_id)
            else:
                data = sess.query(UserModel).all()

        result = {"data": {"user": [UserBaseSchema().dump(item) for item in data]}}
        return result


class UserSignUpResource(BaseUserResource):
    @validate_schema(UserSignUpSchema)
    def post(self):
        data = request.json

        password_hash, password_salt = \
            self.generate_password_hash_and_salt(data["password"])
        del data["password"]
        data["password_hash"] = password_hash
        data["password_salt"] = password_salt

        user = UserModel(**data)

        with Session(engine) as con:
            con.add(user)
            token = self.generate_token(user.id)
            con.commit()

        user_response = UserBaseSchema().dump(data)

        result = {
            "user": user_response,
            "token": token,
        }
        return result, 201


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

