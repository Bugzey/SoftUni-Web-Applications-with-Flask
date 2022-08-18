import sqlalchemy as db
from sqlalchemy.orm import(
    declarative_base,
    Session,
)

from lecture6.config import URL

engine = db.create_engine(URL)
metadata = db.MetaData(schema = "lecture6")

class BaseBase:
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    created_date = db.Column(
        db.DateTime, server_default = db.func.now(), nullable = False,
    )
    updated_time = db.Column(
        db.DateTime,
        server_default = db.func.now(),
        nullable = False,
        onupdate = db.func.now(),
    )

Base = declarative_base(cls = BaseBase, metadata = metadata)

class RoleModel(Base):
    __tablename__ = "role"
    role = db.Column(db.String(255), nullable = False)


class StatusModel(Base):
    __tablename__ = "status"
    status = db.Column(db.String(255), nullable = False)


class UserModel(Base):
    __tablename__ = "user"
    first_name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False, unique = True)
    phone = db.Column(db.String(255), nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable = False)


class ComplaintModel(Base):
    __tablename__ = "complaint"
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    amount= db.Column(db.Float, nullable=False)
    status_id = db.Column( db.Integer, db.ForeignKey("status.id"), nullable=False)
    status = db.orm.relationship(StatusModel)
    complainer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complainer = db.orm.relationship(UserModel)

