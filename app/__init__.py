from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
Bootstrap(app)
db = SQLAlchemy(app)
db.Model.metadata.reflect(bind=db.engine)

from app import routes
