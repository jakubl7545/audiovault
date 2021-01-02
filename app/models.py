from app import app
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
Base = declarative_base()
Base.metadata.reflect(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Content(Base):
	__table__ = Base.metadata.tables['content']

class Users(Base):
	__table__ = Base.metadata.tables['users']
