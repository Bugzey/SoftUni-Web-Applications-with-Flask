import datetime as dt
from hashlib import scrypt
import os

from flask import request
from flask_restful import Resource
import jwt
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
        user: UserModel,
        valid_time: dt.timedelta = dt.timedelta(days = 1),
    ):
        payload = {
            "sub": user.id,
            "iat": dt.datetime.now(),
            "exp": dt.datetime.now() + valid_time,
        }
        token = jwt.encode(payload, key = SECRET, algorithm = "HS256")
        return token

    @staticmethod
    def validate_token(
        user: UserModel,
        token: str,
    ):
        try:
            decoded_token = jwt.decode(token, key = SECRET)
        except jwt.InvalidTokenError:
            return False

        if decoded_token["sub"] != user.id:
            return False

        return True


class UserInfoResource(BaseUserResource):
    def get(self, user_id: int):
        #   TODO: return user info only for a registered user
        pass

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
            token = self.generate_token(user)
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
