from app import app, db, login
from flask import render_template, redirect, url_for, request, send_file
from flask_login import current_user, login_user, logout_user, login_required
from .forms import *
from .models import Users, Content, Featured, News
from .description_generator import get_description
from datetime import datetime
from os import remove, replace

login.login_view = 'login'

@app.route('/')
def index():
	featured = Content.query.join(Featured).with_entities(Content.id, Content.title, Content.description).order_by(Featured.id).all()
	news = News.query.order_by(News.id.desc())
	recent_shows = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
		downloaded=1).filter_by(type='show').order_by(Content.updated_at.desc()).limit(app.config['RECENTLY_ADDED'])
	recent_movies = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
		downloaded=1).filter_by(type='movie').order_by(Content.updated_at.desc()).limit(app.config['RECENTLY_ADDED'])
	return render_template('index.html', featured=featured, shows=recent_shows, movies=recent_movies, news=news)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	error = None
	next = request.args.get('next')
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			error = 'Invalid username or password'
		else:
			login_user(user, remember=form.rememberMe.data)
			return redirect(next or url_for('index'))
	return render_template('login.html', form=form, error=error)

@app.route('/logout')
def logout():
	logout_user()
	return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = Users(name=form.name.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/<content_type>')
def content(content_type):
	search_by_date_form = SearchByDateForm(request.args)
	search_form = SearchForm(request.args)
	page=request.args.get('page', 1, type=int)
	if content_type == 'downloaded':
		entries = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
			downloaded=1).order_by(Content.title).paginate(page, app.config['ITEMS_PER_PAGE'], False)
		if 'date' in request.args:
			entries = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
				downloaded=1).filter(Content.created_at >= request.args.get('date')).order_by(
				Content.title).paginate(page, app.config['ITEMS_PER_PAGE'], False)
		elif 'search' in request.args:
			entries = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
				downloaded=1).filter(Content.title.like("%" + request.args.get('search') + "%")).order_by(
				Content.title).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	elif content_type == 'failed':
		entries = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
			failed=1).order_by(Content.title).paginate(page, app.config['ITEMS_PER_PAGE'], False)
		if 'date' in request.args:
			entries = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
				failed=1).filter(Content.created_at >= request.args.get('date')).order_by(
				Content.title).paginate(page, app.config['ITEMS_PER_PAGE'], False)
		elif 'search' in request.args:
			entries = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
				failed=1).filter(Content.title.like("%" + request.args.get('search') + "%")).order_by(
				Content.title).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	else:
		entries = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
		downloaded=1).filter_by(type=content_type[:-1]).order_by(Content.title).paginate(page, app.config['ITEMS_PER_PAGE'], False)
		if 'date' in request.args:
			entries = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
			downloaded=1).filter_by(type=content_type[:-1]).filter(Content.created_at>=request.args.get('date')).order_by(Content.title).paginate(page, app.config['ITEMS_PER_PAGE'], False)
		elif 'search' in request.args:
			entries = Content.query.with_entities(Content.id, Content.title, Content.description).filter_by(
			downloaded=1).filter_by(type=content_type[:-1]).filter(Content.title.like("%"+request.args.get('search')+"%")).order_by(Content.title).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	return render_template('content.html', content_type=content_type, entries=entries, search_by_date_form=search_by_date_form, search_form=search_form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if current_user.is_anonymous or not current_user.is_admin:
		return '<h1>You are not authorized to view this content</h1>'
	form = UploadForm()
	if form.generate_description.data:
		form.description.data = get_description(form.name.data)
	if form.submit.data and form.validate_on_submit():
		uploaded_file = request.files['file']
		if form.type.data == 'movie':
			file_path = ''.join((app.config['PATH_FOR_MOVIES'], uploaded_file.filename))
			uploaded_file.save(file_path)
		elif form.type.data == 'show':
			file_path = ''.join((app.config['PATH_FOR_SHOWS'], uploaded_file.filename))
			uploaded_file.save(file_path)
		content = Content(title=form.name.data, type=form.type.data, description=form.description.data, file_path=file_path)
		db.session.add(content)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('upload.html', form=form)

@app.route('/download/<id>')
@login_required
def download(id):
	file_path = Content.query.with_entities(Content.file_path).filter_by(id=id).first()[0]
	return send_file(file_path, as_attachment=True)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
	if current_user.is_anonymous or not current_user.is_admin:
		return '<h1>You are not authorized to view this content</h1>'
	form = DeleteForm()
	name = Content.query.with_entities(Content.title).filter_by(id=id).first()[0]
	if form.yes.data:
		deleted_item = Content.query.filter_by(id=id).first()
		db.session.delete(deleted_item)
		db.session.commit()
		if deleted_item.file_path is not None:
			remove(deleted_item.file_path)
		return redirect(url_for('index'))
	elif form.no.data:
		return redirect(url_for('index'))
	return render_template('delete.html', form=form, name=name)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
	if current_user.is_anonymous or not current_user.is_admin:
		return '<h1>You are not authorized to view this content</h1>'
	item = Content.query.with_entities(Content.title, Content.type, Content.description, Content.file_path).filter_by(id=id).first()
	form = EditForm(obj=item)
	if form.validate_on_submit():
		if item.file_path != form.file_path.data:
			replace(item.file_path, form.file_path.data)
		Content.query.filter_by(id=id).update(
		{Content.title: form.title.data, Content.type: form.type.data, Content.description: form.description.data,
		Content.file_path: form.file_path.data, Content.updated_at: datetime.utcnow()})
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('edit.html', form=form)

@app.route('/add/<id>', methods=['GET', 'POST'])
def add(id):
	if current_user.is_anonymous or not current_user.is_admin:
		return '<h1>You are not authorized to view this content</h1>'
	if Featured.query.count() == app.config['NUMBER_OF_FEATURED']:
		deleted_item = Featured.query.order_by(Featured.id).first()
		db.session.delete(deleted_item)
	featured = Featured(content_id=id)
	db.session.add(featured)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/news', methods=['GET', 'POST'])
def news():
	form = NewsForm()
	if form.validate_on_submit():
		news = News(content=form.content.data)
		db.session.add(news)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('news.html', form=form)
