from typing import (
    Any,
)

from werkzeug.security import check_password_hash, generate_password_hash

from lecture6.db import sess
from lecture6.managers.auth import AuthManager
from lecture6.models import (UserModel, RoleModel)

class UserManager:
    @staticmethod
    def register(complainer_data: dict[str, Any]):
        """
        Hashes the plain password
        :param complainer_data: dict
        :return: complainer
        """
        complainer_data["password_hash"] = generate_password_hash(
            complainer_data['password'], method='sha256'
        )
        del complainer_data["password"]

        complainer = UserModel(**complainer_data)
        default_role = sess.query(RoleModel) \
            .where(RoleModel.role == "complainer").first()
        complainer.role_id = default_role.id
        sess.add(complainer)
        token = AuthManager.encode_token(complainer)
        return token

    @staticmethod
    def login(data: dict[str, str]) -> str:
        """
        Checks the email and password (hashes the plain password)
        :param data: dict -> email, password
        :return: token
        """
        complainer = sess \
            .query(UserModel) \
            .where(UserModel.email == data["email"]) \
            .first()

        if complainer and check_password_hash(complainer.password_hash, data["password"]):
            return AuthManager.encode_token(complainer)

        return "Invalid username or password", 401

