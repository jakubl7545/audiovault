from app import app, db, login
from flask_login import UserMixin

class Content(db.Model):
	__table__ = db.Model.metadata.tables['content']

class Users(UserMixin, db.Model):
	__table__ = db.Model.metadata.tables['users']
	def get_id(self):
		return self.user_id

@login.user_loader
def load_user(id):
	return Users.query.get(int(id))
