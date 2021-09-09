from app import app

test_client = app.test_client()

def test_home_page():
	response = test_client.get('/')
	assert response.status_code == 200
	assert b"Welcome to the AudioVault" in response.data

def test_register_page():
	response = test_client.get('/register')
	assert response.status_code == 200
	assert b"<h1>Register</h1>" in response.data

def test_login_page():
	response = test_client.get('/login')
	assert response.status_code == 200
	assert b"<h1>Log in</h1>" in response.data

def test_shows_page():
	response = test_client.get('/shows')
	assert response.status_code == 200
	assert b"<h1>View shows</h1>" in response.data

def test_movies_page():
	response = test_client.get('/movies')
	assert response.status_code == 200
	assert b"<h1>View movies</h1>" in response.data

def test_upload_page():
	response = test_client.get('/upload')
	assert response.status_code == 200
	assert b'not authorized' in response.data

