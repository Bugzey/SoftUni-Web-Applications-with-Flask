from flask import (
    Flask,
    request,
)
from flask_restful import Resource, Api
import os
import sqlalchemy as db
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    Session,
)

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABSE_URI"] =
engine = db.create_engine(
    "postgresql://{user}:{password}@{server}:{port}/{database}".format(
        user = os.environ["USER"],
        password = os.environ["PASSWORD"],
        server = os.environ["SERVER"],
        port = os.environ["PORT"],
        database = os.environ["DATABASE"],
    )
)
api = Api(app)
Base = declarative_base()

class BookModel(Base):
    __tablename__ = "books"
    pk = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    author = db.Column(db.String)

    def __repr__(self):
        return f"<{self.pk}: {self.tittle} from {self.author}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Books(Resource):
    def post(self):
        data = request.get_json()
        new_book = BookModel(**data)
        
        with Session(engine) as con:
            con.add(new_book)
            con.commit()
            return new_book.as_dict()

#   Create all??
Base.metadata.create_all(engine)
api.add_resource(Books, "/books/")


if __name__ == "__main__":
    app.run()

