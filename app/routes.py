from flask import render_template, redirect, url_for
from app import app, db
from .forms import *
from .models import Users, Content

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
		user = Users(name=form.name.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/<content_type>')
def content(content_type):
	items = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(type=content_type[:-1]).all()
	return(render_template('content.html', content_type=content_type, items=items))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		content = Content(title=form.name.data, type=form.type.data, description=form.description.data)
		db.session.add(content)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('upload.html', form=form)

@app.route('/delete/<id>')
def delete(id):
	deleted_item = Content.query.filter_by(id=id).first()
	db.session.delete(deleted_item)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
	item = Content.query.with_entities(Content.title, Content.type, Content.description).filter_by(id=id).first()
	form = EditForm(obj=item)
	if form.validate_on_submit():
		Content.query.filter_by(id=id).update(
		{Content.title: form.title.data, Content.type: form.type.data, Content.description: form.description.data})
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('edit.html', form=form)
