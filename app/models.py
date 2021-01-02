from app import app
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
Base = declarative_base()
Base.metadata.reflect(engine)

class Content(Base):
	__table__ = Base.metadata.tables['content']

class Users(Base):
	__table__ = Base.metadata.tables['users']
