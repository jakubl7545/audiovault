from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField, SearchField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, StopValidation
from flask_wtf import FlaskForm as Form
from app import db
from flask_login import current_user
from .models import Content, Users

class UploadForm(Form):
	name = StringField('Name', [DataRequired()])
	type = SelectField('Type', [DataRequired()], choices=['movie', 'show'])
	description = TextAreaField('Description', [DataRequired()])
	file = FileField('Choose a field', [FileRequired(), FileAllowed(['mp3', 'zip'])])
	submit = SubmitField('Upload')

	def validate_name(self, name):
		content = Content.query.with_entities(Content.title).filter_by(title=name.data).first()
		if content is not None:
			raise ValidationError('This item is already uploaded')

class LoginForm(Form):
	email = StringField('E-mail address', [Email(), DataRequired()])
	password = PasswordField('Password', [DataRequired()])
	rememberMe = BooleanField('Remember me')
	submit = SubmitField('Log in')

	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('Your email is invalid')

	def validate_password(self, password):
		user = Users.query.filter_by(email=self.email.data).first()
		if user is None:
			raise StopValidation()
		elif not user.check_password(password.data):
			raise ValidationError('Your password is invalid')

class RegisterForm(Form):
	name = StringField('User name', [DataRequired()])
	email = StringField('E-mail address', [Email(), DataRequired()])
	password = PasswordField('Password', [DataRequired()])
	confirmPassword = PasswordField('Confirm password', [EqualTo('password'), DataRequired()])
	submit = SubmitField('Register')

	def validate_name(self, name):
		user = Users.query.with_entities(Users.name).filter_by(name=name.data).first()
		if user is not None:
			raise ValidationError('Please use a different username')

	def validate_email(self, email):
		user = Users.query.with_entities(Users.email).filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different e-mail address')

class ChangeForm(Form):
	current_password = PasswordField('Current password', [DataRequired()])
	new_password = PasswordField('New password', [DataRequired()])
	confirm_password = PasswordField('Confirm new password', [EqualTo('new_password'), DataRequired()])
	submit = SubmitField('Change password')

	def validate_current_password(self, current_password):
		user = Users.query.filter_by(id=current_user.id).first()
		if not user.check_password(current_password.data):
			raise ValidationError('Your current password is invalid')

class EditForm(Form):
	title = StringField('Title', [DataRequired()])
	type = SelectField('Type', [DataRequired()], choices=['movie', 'show'])
	description = TextAreaField('Description', [DataRequired()])
	file_path = StringField('File path', [DataRequired()])
	submit = SubmitField('Edit')

class SearchByDateForm(Form):
	date = DateField('From date')

class SearchForm(Form):
	search = SearchField('Enter the title')

class NewsForm(Form):
	content = TextAreaField('Text', [DataRequired()])
	submit = SubmitField('Send')

class DeleteForm(Form):
	yes = SubmitField('Yes')
	no = SubmitField('no')

class ModifyForm(Form):
	content = TextAreaField('Text', [DataRequired()])
	submit = SubmitField('Modify')
