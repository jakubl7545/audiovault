from app import app, db, login, bcrypt
from flask_login import UserMixin
import jwt
from time import time

class Content(db.Model):
	__table__ = db.Model.metadata.tables['content']

class Featured(db.Model):
	__table__ = db.Model.metadata.tables['featured']

class Users(UserMixin, db.Model):
	__table__ = db.Model.metadata.tables['users']
	def get_id(self):
		return self.id

	def set_password(self, password):
		self.password = bcrypt.generate_password_hash(password)

	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256'
		)

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
		except:
			return
		return Users.query.get(id)

@login.user_loader
def load_user(id):
	return Users.query.get(int(id))

class News(db.Model):
	__table__ = db.Model.metadata.tables['news']
