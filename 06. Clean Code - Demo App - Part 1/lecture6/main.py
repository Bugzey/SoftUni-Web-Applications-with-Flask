from flask import Flask
from flask_restful import Api

from lecture6.db import sess
from lecture6.resources.routes import routes

app = Flask(__name__)
api = Api(app)

[api.add_resource(*route) for route in routes]

@app.after_request
def commit_changes(response):
    sess.commit()
    return response

if __name__ == '__main__':
    app.run()

