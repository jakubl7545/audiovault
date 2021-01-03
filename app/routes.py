from flask import render_template, redirect, url_for
from app import app
from .forms import *
from .models import session, Users, Content

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
	shows = session.query(Content.id, Content.title, Content.description).filter_by(type='show').all()
	return render_template('shows.html', shows=shows)

@app.route('/movies')
def movies():
	movies = session.query(Content.id, Content.title, Content.description).filter_by(type='movie').all()
	return render_template('movies.html', movies=movies)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		content = Content(title=form.name.data, type=form.type.data, description=form.description.data)
		session.add(content)
		session.commit()
		return redirect(url_for('index'))
	return render_template('upload.html', form=form)

@app.route('/delete/<id>')
def delete(id):
	deleted_item = session.query(Content).filter_by(id=id).first()
	session.delete(deleted_item)
	session.commit()
	return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
	item = session.query(Content.title, Content.type, Content.description).filter_by(id=id).first()
	form = EditForm(obj=item)
	if form.validate_on_submit():
		session.query(Content).filter_by(id=id).update(
		{Content.title: form.title.data, Content.type: form.type.data, Content.description: form.description.data})
		session.commit()
		return redirect(url_for('index'))
	return render_template('edit.html', form=form)
