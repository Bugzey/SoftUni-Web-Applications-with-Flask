import datetime as dt

from flask_httpauth import HTTPTokenAuth
import jwt

from lecture6.config import SECRET
from lecture6.models import (db, UserModel, sess)

class AuthManager:
    @staticmethod
    def encode_token(user: UserModel):
        payload = {
            "sub": user.id,
            "exp": dt.datetime.utcnow() + dt.timedelta(days=2),
            "type": user.role_id,
        }
        return jwt.encode(payload, key=SECRET, algorithm="HS256")

    @staticmethod
    def decode_token(token: str) -> tuple[str,str]:
        try:
            info = jwt.decode(jwt=token, key=SECRET,  algorithms=["HS256"])
            return info['sub'], info["type"]
        except Exception as ex:
            raise ex


auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    try:
        user_id, type_user = AuthManager.decode_token(token)
        user = sess.get(UserModel, user_id)
        return user
    except Exception as ex:
        return "Invalid or missing token", 400

