import os

from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine

from lecture5.config import URL
from lecture5.models import engine
from lecture5.resources import (
    UserSignUpResource,
)

#   TODO: import resources and register here

engine = create_engine(URL)
app = Flask(__name__)
api = Api(app)

api.add_resource(UserSignUpResource, "/signup/")

