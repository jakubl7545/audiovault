import os
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
import unittest
from flask import current_app
from app import app, db
from app.models import Users
from flask_login import current_user


class TestUsers(unittest.TestCase):
	def setUp(self):
		self.app = app
		self.app.config['WTF_CSRF_ENABLED'] = False
		self.appctx = self.app.app_context()
		self.appctx.push()
		db.create_all()
		self.create_users()
		self.client = self.app.test_client()

	def tearDown(self):
		self.appctx.pop()
		self.app = None
		self.appctx = None
		self.client = None

	def create_users(self):
		user = Users(name='user1', email='user1@mail.com')
		user.set_password('Password1')
		db.session.add(user)
		new_user = Users(name='user2', email='user2@mail.com')
		new_user.set_password('Password2')
		db.session.add(new_user)
		db.session.commit()

	def test_user_model(self):
		user = Users(name='user3', email='user3@mail.com', is_admin=True)
		assert user.name == 'user3'
		assert user.email == 'user3@mail.com'
		assert user.is_admin is True

	def test_password_hashing(self):
		user = Users(name='user3', email='user3@mail.com')
		user.set_password('Password3')
		assert user.check_password('Password') is False
		assert user.check_password('Password3') is True

	def test_register_form(self):
		response = self.client.get('/register')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="name"' in html
		assert 'name="email"' in html
		assert 'name="password"' in html
		assert 'name="confirmPassword"' in html
		assert 'name="submit"' in html

	def test_register_user(self):
		with self.client:
			response = self.client.post('/register', data = {
				'name': 'jakub', 'email': 'jakub@mail.com', 'password': 'Password123!', 'confirmPassword': 'Password123!'
			}, follow_redirects=True)
			assert response.status_code == 200
			assert response.request.path == '/'
			assert current_user.name == 'jakub'

	def test_register_user_with_passwords_not_matching(self):
		response = self.client.post('/register', data={
			'name': 'jakub', 'email': 'jakub@mail.com', 'password': 'foo', 'confirmPassword': 'bar'
		})
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'Field must be equal to password.' in html

	def test_validate_user_name_when_registering(self):
		response = self.client.post('/register', data = {
			'name': 'user1', 'email': 'user@mail.com', 'password': 'Password1!'
		})
		html = response.get_data(as_text=True)
		assert 'Please use a different username' in html

	def test_validate_user_email_when_registering(self):
		response = self.client.post('/register', data = {
			'name': 'user2', 'email': 'user1@mail.com', 'password': 'Password2'
		})
		html = response.get_data(as_text=True)
		assert 'Please use a different e-mail address' in html

	def test_login_form(self):
		response = self.client.get('/login')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="email"' in html
		assert 'name="password"' in html
		assert 'name="rememberMe"' in html
		assert 'name="submit"' in html

	def test_login_user(self):
		with self.client:
			response = self.client.post('/login', data = {
				'email': 'user1@mail.com', 'password': 'Password1'
			}, follow_redirects=True)
			assert response.status_code == 200
			assert response.request.path == '/'
			assert current_user.name == 'user1'

	def test_validate_user_email_when_loging(self):
		response = self.client.post('/login', data = {
			'email': 'user@mail.com', 'password': 'Password1'
		})
		html = response.get_data(as_text=True)
		assert 'Your email is invalid' in html

	def test_validate_user_password_when_login(self):
		response = self.client.post('login', data = {
			'email': 'user1@mail.com', 'password': 'Password'
		})
		html = response.get_data(as_text=True)
		assert 'Your password is invalid' in html

	def test_logout_user(self):
		with self.client:
			response = self.client.post('/login', data = {
				'email': 'user1@mail.com', 'password': 'Password1'
			}, follow_redirects=True)
			response = self.client.get('/logout', follow_redirects=True)
			html = response.get_data(as_text=True)
			assert response.status_code == 200
			assert response.request.path == '/'
			assert 'Log in' in html
			assert current_user.is_anonymous is True

	def test_user_authentication(self):
		with self.client:
			response = self.client.post('/login', data = {
				'email': 'user1@mail.com', 'password': 'Password1'
			}, follow_redirects=True)
			html = response.get_data(as_text=True)
			assert 'Log out' in html
			assert 'Upload' not in html
			assert current_user.is_authenticated is True

	def test_change_password_form(self):
		response = self.client.get('/change_password')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="current_password"' in html
		assert 'name="new_password"' in html
		assert 'name="confirm_password"' in html
		assert 'name="submit"' in html

	def test_change_password(self):
		response = self.client.post('/login', data = {
			'email': 'user2@mail.com', 'password': 'Password2'
		}, follow_redirects=True)
		response = self.client.post('/change_password', data = {
			'current_password': 'Password2', 'new_password': 'Password3', 'confirm_password': 'Password3'
		}, follow_redirects=True)
		assert response.status_code == 200
		assert response.request.path == '/'

	def test_validate_current_password_when_changing(self):
		response = self.client.post('login', data = {
			'email': 'user1@mail.com', 'password': 'Password1'
		}, follow_redirects=True)
		response = self.client.post('change_password', data = {
			'current_password': 'Password2', 'new_password': 'Password1!', 'confirm_password': 'Password1!'
		}, follow_redirects=True)
		html = response.get_data(as_text=True)
		assert 'password you entered does not match' in html

	def test_validate_new_password_when_changing(self):
		response = self.client.post('login', data = {
			'email': 'user1@mail.com', 'password': 'Password1'
		}, follow_redirects=True)
		response = self.client.post('change_password', data = {
			'current_password': 'Password1', 'new_password': 'Password1!', 'confirm_password': 'Password2'
		}, follow_redirects=True)
		html = response.get_data(as_text=True)
		assert 'Field must be equal to new_password.' in html

	def test_reset_password_request_form(self):
		response = self.client.get('/reset_password_request')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="email"' in html
		assert 'name="submit"' in html
