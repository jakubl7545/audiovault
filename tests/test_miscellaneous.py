import os
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
os.environ['RECENTLY_ADDED'] = '5'
os.environ['ITEMS_PER_PAGE'] = '10'
os.environ['PATH_FOR_MOVIES'] = '/audiovault/movies'
import unittest
from flask import current_app
from app import app, db
from app.models import News, Users
from datetime import date


class TestMiscellaneous(unittest.TestCase):
	def setUp(self):
		self.app = app
		self.app.config['WTF_CSRF_ENABLED'] = False
		self.appctx = self.app.app_context()
		self.appctx.push()
		db.create_all()
		self.create_user()
		self.client = self.app.test_client()

	def tearDown(self):
		db.drop_all()
		self.appctx.pop()
		self.app = None
		self.appctx = None
		self.client = None

	def create_user(self):
		user = Users(name='user1', email='user1@mail.com', is_admin=True)
		user.set_password('Password1')
		db.session.add(user)
		db.session.commit()

	def login_user(self):
		response = self.client.post('/login', data={
			'email': 'user1@mail.com', 'password': 'Password1'
		}, follow_redirects=True)

	def test_app(self):
		assert self.app is not None
		assert current_app == self.app

	def test_config_variables(self):
		assert current_app.config['RECENTLY_ADDED'] == 5
		assert current_app.config['ITEMS_PER_PAGE'] == 10
		assert current_app.config['PATH_FOR_MOVIES'] == '/audiovault/movies'

	def test_app_extensions(self):
		assert current_app.extensions['bootstrap'] is not None
		assert current_app.extensions['mail'] is not None
		assert current_app.extensions['migrate'] is not None

	def test_main_page(self):
		response = self.client.get('/')
		html = response.get_data(as_text=True)
		assert response.status_code == 200
		assert 'Welcome to the AudioVault' in html
		assert 'View downloaded' in html

	def test_contact_page(self):
		response = self.client.get('/contact')
		html = response.get_data(as_text=True)
		assert response.status_code == 200
		assert 'Contact us' in html

	def test_news_model(self):
		news = News(content='News text', created_at=date.today())
		assert news.content == 'News text'
		assert news.created_at == date.today()

	def test_news_form(self):
		self.login_user()
		response = self.client.get('/news')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="content"' in html
		assert 'name="submit"' in html

	def  test_add_news(self):
		self.login_user()
		response = self.client.post('/news', data = {'content': 'New info'}, follow_redirects=True)
		html = response.get_data(as_text=True)
		assert response.status_code == 200
		assert response.request.path == '/'
		assert 'New info' in html
		assert f'{date.today()}' in html

	def test_add_news_unauthorized_access(self):
		response = self.client.get('/news')
		html = response.get_data(as_text=True)
		assert 'not authorized' in html

	def test_modify_news_form(self):
		self.login_user()
		response = self.client.post('/news', data={'content': 'New info'}, follow_redirects=True)
		response = self.client.get('/modify/1')
		html = response.get_data(as_text=True)
		assert response.status_code == 200
		assert 'name="content"' in html
		assert 'name="submit"' in html

	def test_modify_news(self):
		self.login_user()
		response = self.client.post('/news', data={'content': 'New info'}, follow_redirects=True)
		response = self.client.post('/modify/1', data={'content': 'Info updated'}, follow_redirects=True)
		html = response.get_data(as_text=True)
		assert response.status_code == 200
		assert response.request.path == '/'
		assert 'Info updated' in html

	def test_modify_news_unauthorized_access(self):
		response = self.client.get('/modify/1')
		html = response.get_data(as_text=True)
		assert 'not authorized' in html

	def test_remove_news(self):
		self.login_user()
		response = self.client.post('/news', data={'content': 'New info'}, follow_redirects=True)
		response = self.client.post('/remove', data={'id': 1, 'type': 'news'}, follow_redirects=True)
		response = self.client.get('/')
		html = response.get_data(as_text=True)
		assert 'New info' not in html
