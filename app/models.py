from app import app, db, login, bcrypt
from flask_login import UserMixin

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

@login.user_loader
def load_user(id):
	return Users.query.get(int(id))

class News(db.Model):
	__table__ = db.Model.metadata.tables['news']
