import sqlalchemy as db
from sqlalchemy.orm import (
    declarative_base,
)

from lecture5.config import URL
engine = db.create_engine(URL)
metadata = db.MetaData(schema = "lecture5")

class BaseModel:
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    created_time = db.Column(db.DateTime, nullable = False, default = db.func.now())
    updated_time = db.Column(
        db.DateTime, nullable = False, default = db.func.now(), onupdate = db.func.now()
    )

Base = declarative_base(cls = BaseModel, metadata = metadata)

class UserModel(Base):
    __tablename__ = "user"
    username = db.Column(db.String(255), nullable = False, unique = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password_hash = db.Column(db.LargeBinary, nullable = False)
    password_salt = db.Column(db.LargeBinary, nullable = False)

