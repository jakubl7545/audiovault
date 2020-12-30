from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

from flask_wtf import Form

class UploadForm(Form):
	name = StringField('Name', [DataRequired()])
	type = SelectField('Type', [DataRequired()], choices=['movie', 'show'])
	description = TextAreaField('Description', [DataRequired()])
	submit = SubmitField('Upload')

class LoginForm(Form):
	email = StringField('E-mail address', [Email(), DataRequired()])
	password = PasswordField('Password', [DataRequired()])
	rememberMe = BooleanField('Remember me')
	submit = SubmitField('Log in')

class RegisterForm(Form):
	name = StringField('Name', [DataRequired()])
	email = StringField('E-mail address', [Email(), DataRequired()])
	password = PasswordField('Password', [DataRequired()])
	confirmPassword = PasswordField('Confirm password', [EqualTo('password'), DataRequired()])
	submit = SubmitField('Register')