from flask import render_template, redirect, url_for
from app import app
from .forms import *

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		return redirect(url_for('index'))
	return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/shows')
def shows():
	return render_template('shows.html')

@app.route('/movies')
def movies():
	return render_template('movies.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		return redirect(url_for('index'))
	return render_template('upload.html', form=form)
