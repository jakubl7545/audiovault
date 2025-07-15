import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db, login, bcrypt
from flask_login import UserMixin
import jwt
from time import time
from datetime import date, datetime, timezone

# The following is not a password
password_reset_algorithm = 'HS256'  # nosec

class Content(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	title: so.Mapped[str] = so.mapped_column(sa.String(100))
	type: so.Mapped[str] = so.mapped_column(sa.String(10))
	description: so.Mapped[str] = so.mapped_column(sa.Text)
	created_at: so.Mapped[date] = so.mapped_column(default=lambda: date.today())
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	downloaded: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
	failed: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
	file_path: so.Mapped[str] = so.mapped_column(sa.String(100))

	featured: so.Mapped['Featured'] = so.relationship(back_populates='content', uselist=False, passive_deletes=True)

class Featured(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	content_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Content.id), unique=True)

	content: so.Mapped[Content] = so.relationship(back_populates='featured')

class Users(UserMixin, db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	name: so.Mapped[str] = so.mapped_column(sa.String(50))
	email: so.Mapped[str] = so.mapped_column(sa.String(50))
	password: so.Mapped[str] = so.mapped_column(sa.String(255))
	is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

	def get_id(self):
		return self.id

	def set_password(self, password):
		self.password = bcrypt.generate_password_hash(password)

	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm=password_reset_algorithm
		)

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[password_reset_algorithm])['reset_password']
		except:
			return
		return db.session.get(Users, id)

@login.user_loader
def load_user(id):
	return db.session.get(Users, int(id))

class News(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	content: so.Mapped[str] = so.mapped_column(sa.Text)
	created_at: so.Mapped[date] = so.mapped_column(default=lambda: date.today())
