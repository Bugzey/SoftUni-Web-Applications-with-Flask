import sqlalchemy as db
from sqlalchemy.orm import declarative_base

from lecture6.config import URL

engine = db.create_engine(URL)
metadata = db.MetaData(schema = "lecture6")

class BaseBase:
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    created_date = db.Column(db.DateTime, default = db.func.now(), nullable = False)
    updated_teim = db.Column(
        db.DateTime,
        default = db.func.now(),
        nullable = False,
        onupdate = db.func.now(),
    )

Base = declarative_base(cls = BaseBase)

class RoleModel(Base):
    role = db.Column(db.String(255), nullable = False)

class StatusModel(Base):
    status = db.Column(db.String(255), nullable = False)

