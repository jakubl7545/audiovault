from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
Bootstrap(app)
db = SQLAlchemy(app)
app.app_context().push()
db.Model.metadata.reflect(bind=db.engine)
login = LoginManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

from app import routes
