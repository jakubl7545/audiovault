from flask import render_template, redirect, url_for
from app import app
from .forms import *
from sqlalchemy.orm import sessionmaker
from .models import engine, Users, Content

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
	Session = sessionmaker(bind=engine)
	session = Session()
	shows = session.query(Content.title, Content.description).filter_by(type='show').all()
	return render_template('shows.html', shows=shows)

@app.route('/movies')
def movies():
	Session = sessionmaker(bind=engine)
	session = Session()
	movies = session.query(Content.title, Content.description).filter_by(type='movie').all()
	return render_template('movies.html', movies=movies)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		return redirect(url_for('index'))
	return render_template('upload.html', form=form)
