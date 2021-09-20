from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField, SearchField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm as Form
from app import db
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
