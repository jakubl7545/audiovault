from flask import render_template
from app import app

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/shows')
def shows():
	return render_template('shows.html')

@app.route('/movies')
def movies():
	return render_template('movies.html')

@app.route('/upload')
def upload():
	return render_template('upload.html')
