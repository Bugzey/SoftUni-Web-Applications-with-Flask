import sqlalchemy as db
from sqlalchemy.orm import(
    Session,
)

from lecture6.config import URL

engine = db.create_engine(URL)
sess = Session(engine)

