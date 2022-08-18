from flask_restful import Resource
from flask import request

from lecture6.managers.user import UserManager
from lecture6.schemas.request.user import (
    RequestLoginUserSchema,
    RequestRegisterUserSchema,
)
from lecture6.utils.decorators import validate_schema


class RegisterUser(Resource):
    @validate_schema(RequestRegisterUserSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return {"token": token}, 201


class LoginUser(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {"token": token, "role": "complainer" }

