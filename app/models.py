from app import app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Content(db.Model):
	__table__ = db.Model.metadata.tables['content']

class Users(UserMixin, db.Model):
	__table__ = db.Model.metadata.tables['users']
	def get_id(self):
		return self.user_id
	
	def set_password(self, password):
		self.password = generate_password_hash(password)
	
	def check_password(self, password):
		return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
	return Users.query.get(int(id))
