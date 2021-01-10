from app import app, db

class Content(db.Model):
	__table__ = db.Model.metadata.tables['content']

class Users(db.Model):
	__table__ = db.Model.metadata.tables['users']
