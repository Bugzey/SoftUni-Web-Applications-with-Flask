"""
Separate models library for lecture 4
"""

import sqlalchemy as db
from sqlalchemy.orm import (
    declarative_base,
    Session,
)

metadata = db.MetaData(schema = "lecture4")
Base = declarative_base(metadata = metadata)

class User(Base):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), nullable = False, unique = True)
    password_hash = db.Column(db.LargeBinary, nullable = False)
    password_salt = db.Column(db.LargeBinary, nullable = False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))


class ClothingItem(Base):
    __tablename__ = "clothing_item"
    clothing_id = db.Column(db.Integer, primary_key = True)


class Colour(Base):
    __tablename__ = "colour"
    colour_id = db.Column(db.Integer, primary_key = True)
    colour = db.Column(db.String(255))


class Size(Base):
    __tablename__ = "size"
    size_id = db.Column(db.Integer, primary_key = True)
    size = db.Column(db.String(10))


