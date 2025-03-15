import os
import tempfile
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
os.environ['PATH_FOR_MOVIES'] = tempfile.gettempdir()
os.environ['SQLALCHEMY_ECHO'] = 'False'
import io
import unittest
from flask import current_app
from app import app, db
from app.models import Users, Content, Featured
from datetime import date, datetime, timezone, timedelta


class TestContent(unittest.TestCase):
	def setUp(self):
		self.app = app
		self.app.config['WTF_CSRF_ENABLED'] = False
		self.appctx = self.app.app_context()
		self.appctx.push()
		db.create_all()
		self.create_user()
		self.client = self.app.test_client()
		self.login_user()

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

	def create_entries(self):
		show = Content(title='Series1', type='show', description='Series1 description', file_path='/audiovault/series1.zip')
		new_show = Content(title='Series2', type='show', description='Series2 description', file_path='/audiovault/series2.zip')
		movie = Content(title='Movie1', type='movie', description='Movie1 description', file_path='/audiovault/movie1.mp3')
		new_movie = Content(title='Movie2', type='movie', description='Movie2 description', file_path='/audiovault/movie2.mp3')
		db.session.add_all([show, new_show, movie, new_movie])
		db.session.commit()

	def login_user(self):
		response = self.client.post('/login', data = {
			'email': 'user1@mail.com', 'password': 'Password1'
		}, follow_redirects=True)

	def test_content_model(self):
		content = Content(title='Series3', type='show', description='Series3 description', file_path='/audiovault/series3.mp3',
		created_at=date.today(), updated_at=datetime.now(timezone.utc), downloaded=True, failed=False)
		assert content.title == 'Series3'
		assert content.type == 'show'
		assert content.description == 'Series3 description'
		assert content.file_path == '/audiovault/series3.mp3'
		assert content.created_at == date.today()
		assert content.updated_at <= datetime.now(timezone.utc)
		assert content.downloaded == True
		assert content.failed == False

	def test_featured_model_relations(self):
		self.create_entries()
		featured = Featured(content_id=1)
		db.session.add(featured)
		db.session.commit()
		featured = db.session.get(Featured, 1)
		assert featured.content_id == 1
		assert featured.content.title == 'Series1'

	def test_upload_form(self):
		response = self.client.get('/upload')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="name"' in html
		assert 'name="type"' in html
		assert 'name="description"' in html
		assert 'name="file"' in html
		assert 'name="submit"' in html

	def test_upload_unauthorized_access(self):
		response = self.client.get('/logout', follow_redirects=True)
		response = self.client.get('/upload')
		html = response.get_data(as_text=True)
		assert 'not authorized' in html

	def test_upload(self):
		response = self.client.post('/upload', data = {
			'name': 'Movie3', 'type': 'movie', 'description': 'Movie3 description', 'file': (io.BytesIO(b'testfile'), 'movie3.mp3')
		}, follow_redirects=True, content_type='multipart/form-data')
		html = response.get_data(as_text=True)
		assert response.status_code == 200
		assert response.request.path == '/'
		assert 'Movie3' in html

	def test_validate_file_ext_when_uploading(self):
		response = self.client.post('/upload', data={
			'name': 'Movie4', 'type': 'movie', 'description': 'Movie4 description', 'file': (io.BytesIO(b'testfile'), 'movie4.avi')
		}, follow_redirects=True, content_type='multipart/form-data')
		html = response.get_data(as_text=True)
		assert 'File does not have an approved extension: mp3, zip' in html

	def test_validate_name_when_uploading(self):
		self.create_entries()
		response = self.client.post('/upload', data = {
			'name': 'Series2', 'type': 'show', 'description': 'Series2 description', 'file': (io.BytesIO(b'testfile'), 'series2.zip')
		}, follow_redirects=True, content_type='multipart/form-data')
		html = response.get_data(as_text=True)
		assert 'This item is already uploaded' in html

	@unittest.skip('')
	def test_generate_description(self):
		response = self.client.post('/generate', data = {'title': 'Shrek'})
		assert 'grumpy ogre' in response.json['description']

	def test_edit_form(self):
		self.create_entries()
		response = self.client.get('/edit/2')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="title"' in html
		assert 'name="type"' in html
		assert 'name="description"' in html
		assert 'name="file_path"' in html
		assert 'name="submit"' in html
		assert 'value="Series2"' in html

	def test_edit_unauthorized_access(self):
		response = self.client.get('/logout', follow_redirects=True)
		response = self.client.get('/edit/1')
		html = response.get_data(as_text=True)
		assert 'not authorized' in html

	def test_edit(self):
		self.create_entries()
		response = self.client.post('/edit/1', data = {
			'title': 'Series1 - Season 1', 'type': 'show', 'description': 'Series1 description', 'file_path': '/audiovault/series1.zip'
		}, follow_redirects=True)
		assert response.status_code == 200
		assert response.request.path == '/'
		html = response.get_data(as_text=True)
		assert 'Series1 - Season 1' in html

	def test_delete_form(self):
		self.create_entries()
		response = self.client.get('/delete/3')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="yes"' in html
		assert 'name="no"' in html
		assert 'Movie1' in html

	def test_delete_unauthorized_access(self):
		response = self.client.get('/logout', follow_redirects=True)
		response = self.client.get('/delete/3')
		html = response.get_data(as_text=True)
		assert 'not authorized' in html

	def test_delete_canceled(self):
		self.create_entries()
		response = self.client.post('/delete/3', data={'no': True}, follow_redirects=True)
		assert response.status_code == 200
		assert response.request.path == '/'
		html = response.get_data(as_text=True)
		assert 'Movie1' in html

	def test_delete(self):
		response = self.client.post('/upload', data={
			'name': 'Movie5', 'type': 'movie', 'description': 'Movie5 description', 'file': (io.BytesIO(b'testfile'), 'movie5.mp3')
		}, follow_redirects=True, content_type='multipart/form-data')
		response = self.client.post('/delete/1', data={'yes': True}, follow_redirects=True)
		assert response.status_code == 200
		assert response.request.path == '/'
		html = response.get_data(as_text=True)
		assert 'Movie5' not in html

	def test_download(self):
		response = self.client.post('/upload', data={
			'name': 'Movie6', 'type': 'movie', 'description': 'Movie6 description', 'file': (io.BytesIO(b'testfile'), 'movie6.mp3')
		}, follow_redirects=True, content_type='multipart/form-data')
		response = self.client.get('/download/1')
		assert response.status_code == 200
		assert b'testfile' in response.data

	def test_add_to_featured(self):
		self.create_entries()
		response = self.client.post('/add', data={'id': 4})
		assert 'Added to featured' in response.json['message']
		response = self.client.get('/')
		html = response.get_data(as_text=True)
		assert 'class="collapsible"' in html

	def test_add_to_featured_twice(self):
		self.create_entries()
		response = self.client.post('/add', data={'id': 4})
		response = self.client.post('/add', data={'id': 4})
		assert 'Already in featured' in response.json['message']

	def test_remove_from_featured(self):
		self.create_entries()
		response = self.client.post('/add', data={'id': 4})
		response = self.client.post('/remove', data={'id': 1, 'type': 'featured'})
		response = self.client.get('/')
		html = response.get_data(as_text=True)
		assert 'class="collapsible"' not in html

	def test_clear_featured(self):
		self.create_entries()
		response = self.client.post('/add', data={'id': 1})
		response = self.client.post('/add', data={'id': 2})
		response = self.client.post('/clear')
		response = self.client.get('/')
		html = response.get_data(as_text=True)
		assert 'class="collapsible"' not in html

	def test_content_on_main_page(self):
		self.create_entries()
		response = self.client.get('/')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'Series2' in html
		assert 'Movie2' in html

	def test_shows_page(self):
		self.create_entries()
		response = self.client.get('/shows')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="date"' in html
		assert 'name="search"' in html
		assert 'Series1' in html
		assert 'Series2' in html
		assert 'Movie1' not in html

	def test_movies_page(self):
		self.create_entries()
		response = self.client.get('/movies')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'Movie1' in html
		assert 'Movie2' in html
		assert 'Series1' not in html

	def test_search(self):
		self.create_entries()
		response = self.client.get('/shows?search=series1')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'Series1' in html
		assert 'Series2' not in html

	def test_search_by_date(self):
		self.create_entries()
		content = Content(title='Series4', type='show', description='Series4 description',
		file_path='/audiovault/series4.zip', created_at=date.today()-timedelta(1))
		db.session.add(content)
		db.session.commit()
		response = self.client.get(f'/shows?date={date.today()}')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'Series1' in html
		assert 'Series2' in html
		assert 'Series4' not in html

	def test_pagination(self):
		self.create_entries()
		response = self.client.get('/downloaded?page=2')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'Series2' in html
		assert 'href="/downloaded?page=1"' in html