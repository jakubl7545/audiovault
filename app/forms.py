from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.fields.html5 import DateField, SearchField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf import Form
from app import db
from .models import Users

class UploadForm(Form):
	name = StringField('Name', [DataRequired()])
	type = SelectField('Type', [DataRequired()], choices=['movie', 'show'])
	description = TextAreaField('Description', [DataRequired()])
	generate_description = SubmitField('Generate description')
	submit = SubmitField('Upload')

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
	submit = SubmitField('Edit')

class SearchByDateForm(Form):
	date = DateField('From date')

class SearchForm(Form):
	search = SearchField('Enter the title')

class NewsForm(Form):
	content = TextAreaField('Text', [DataRequired()])
	submit = SubmitField('Send')