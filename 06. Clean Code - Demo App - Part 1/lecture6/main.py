from flask import Flask
from flask_restful import Api

from lecture6.models import Session, engine, metadata
from lecture6.resources.routes import routes

app = Flask(__name__)
api = Api(app)

[api.add_resource(*route) for route in routes]

if __name__ == '__main__':
    app.run()

