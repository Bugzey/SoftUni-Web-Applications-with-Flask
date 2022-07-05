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
URL = "postgresql://{user}:{password}@{server}:{port}/{database}".format(
    user = os.environ["USER"],
    password = os.environ["PASSWORD"],
    server = os.environ["SERVER"],
    port = os.environ["PORT"],
    database = os.environ["DATABASE"],
)

engine = db.create_engine(URL)
api = Api(app)
Base = declarative_base()

#   Models
#   Do separate these into models.py, please
class BookModel(Base):
    __tablename__ = "books"
    pk = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    description = db.Column(db.String)
    reader_pk = db.Column(db.Integer, db.ForeignKey('readers.pk'))
    reader = relationship('ReaderModel')
    
    def __repr__(self):
        return f"<{self.pk}: {self.tittle} from {self.author}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReaderModel(Base):
    __tablename__ = "readers"
    pk = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    books = relationship("BookModel", backref = "book", lazy = "dynamic")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



#   API resources
class Books(Resource):
    def post(self):
        data = request.get_json()
        new_book = BookModel(**data)

        with Session(engine) as con:
            con.add(new_book)
            con.commit()
            return new_book.as_dict()

class Reader(Resource):
    def post(self):
        data = request.get_json()
        new_reader = ReaderModel(**data)
        with Session(engine) as con:
            con.add(new_reader)
            con.commit()
            return new_reader.as_dict()

    def get(self, reader_pk):
        #   NOTE: this is ugly, fix it
        with Session(engine) as con:
            reader = con.query(ReaderModel).where(ReaderModel.pk == reader_pk).first()

            if "/books/" in request.path:
                return {"data": [book.as_dict() for book in reader.books]}
            else:
                return {"data": [{"reader": reader.as_dict()}]}


#   Create all??
Base.metadata.create_all(engine)
api.add_resource(Books, "/books/")
api.add_resource(
    Reader, 
    "/readers/",
    "/readers/<int:reader_pk>/",
    "/readers/<int:reader_pk>/books/",
)


if __name__ == "__main__":
    app.run()

