"""
Separate models library for lecture 4
"""

import enum
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
    phone = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default = db.func.now())
    updated_on = db.Column(
        db.DateTime, default = db.func.now(), onupdate = db.func.now()
    )


class ClothingItem(Base):
    __tablename__ = "clothing_item"
    clothing_item_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique = True, nullable = False)
    photo_url = db.Column(db.String(255), nullable = False)
    created_on = db.Column(db.DateTime, default = db.func.now())
    updated_on = db.Column(
        db.DateTime, default = db.func.now(), onupdate = db.func.now()
    )


class ColourEnum(enum.Enum):
    PINK = "pink"
    BLACK = "black"
    WHITE = "white"
    YELLOW = "yellow"


class Colour(Base):
    __tablename__ = "colour"
    colour_id = db.Column(db.Integer, primary_key = True)
    colour = db.Column(
        db.Enum(ColourEnum), default = ColourEnum.WHITE, nullable = False
    )


class SizeEnum(enum.Enum):
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"


class Size(Base):
    __tablename__ = "size"
    size_id = db.Column(db.Integer, primary_key = True)
    size = db.Column(db.Enum(SizeEnum), default = SizeEnum.S, nullable = False)


class Basket(Base):
    __tablename__ = "basket"
    basket_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    created_on = db.Column(db.DateTime, default = db.func.now())
    updated_on = db.Column(
        db.DateTime, default = db.func.now(), onupdate = db.func.now()
    )

class BasketItem(Base):
    __tablename__ = "basket_item"
    basket_item_id = db.Column(db.Integer, primary_key = True)
    basket_id = db.Column(db.Integer, db.ForeignKey("basket.basket_id"), nullable = False)
    clothing_item_id = db.Column(
        db.Integer, db.ForeignKey("clothing_item.clothing_item_id"), nullable = False
    )
    colour_id = db.Column(
        db.Integer, db.ForeignKey("colour.colour_id"), nullable = False
    )
    size_id = db.Column(
        db.Integer, db.ForeignKey("size.size_id"), nullable = False
    )
    created_on = db.Column(db.DateTime, default = db.func.now())
    updated_on = db.Column(
        db.DateTime, default = db.func.now(), onupdate = db.func.now()
    )

