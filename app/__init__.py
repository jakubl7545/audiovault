from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
Bootstrap(app)
db = SQLAlchemy(app)
db.Model.metadata.reflect(bind=db.engine)
login = LoginManager(app)

from app import routes
