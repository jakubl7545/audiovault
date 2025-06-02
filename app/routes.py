from app import app, db, login
from flask import render_template, redirect, url_for, request, send_file, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from .forms import *
from .models import Users, Content, Featured, News
from .description_generator import get_description
from app.email_generator import send_password_reset_email
from datetime import datetime, timezone
from os import remove as rm
import requests
from shutil import move
from functools import wraps

login.login_view = 'login'

def admin_only(endpoint):
	@wraps(endpoint)
	def decorated_function(*args, **kwargs):
		if current_user.is_anonymous or not current_user.is_admin:
			return '<h1>You are not authorized to view this content</h1><a href="/">Go to home page</a>'
		return endpoint(*args, **kwargs)
	return decorated_function

@app.route('/')
def index():
	featured = db.session.scalars(db.select(Featured).order_by(Featured.id)).all()
	news = db.session.scalars(db.select(News).order_by(News.id.desc()))
	recent_shows = db.session.execute(db.select(Content.id, Content.title, Content.description).filter_by(
		downloaded=1).filter_by(type='show').order_by(Content.updated_at.desc()).limit(app.config['RECENTLY_ADDED']))
	recent_movies = db.session.execute(db.select(Content.id, Content.title, Content.description).filter_by(
		downloaded=1).filter_by(type='movie').order_by(Content.updated_at.desc()).limit(app.config['RECENTLY_ADDED']))
	return render_template('index.html', featured=featured, shows=recent_shows, movies=recent_movies, news=news)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.scalar(db.select(Users).filter_by(email=form.email.data))
		login_user(user, remember=form.rememberMe.data)
		return redirect(url_for('index'))
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

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

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = Users(id=current_user.id)
		user.set_password(form.new_password.data)
		db.session.execute(db.update(Users), [{'id': user.id, 'password': user.password}])
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('change_password.html', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = db.session.scalar(db.select(Users).filter_by(email=form.email.data))
		if user:
			send_password_reset_email(user)
		return redirect(url_for('index'))
	return render_template('reset_password.html', form=form, title='Reset password request')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = Users.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('reset_password.html', form=form, title='Reset password')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/<content_type>')
def content(content_type):
	search_by_date_form = SearchByDateForm(request.args)
	search_form = SearchForm(request.args)
	page=request.args.get('page', 1, type=int)
	if content_type == 'downloaded':
		entries = db.paginate(db.select(Content).filter_by(downloaded=1).order_by(
			Content.title), page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
		if 'date' in request.args:
			entries = db.paginate(db.select(Content).filter_by(downloaded=1).filter(
				Content.created_at >= request.args.get('date')).order_by(Content.title),
				page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
		elif 'search' in request.args:
			entries = db.paginate(db.select(Content).filter_by(downloaded=1).filter(
				Content.title.like("%" + request.args.get('search') + "%")).order_by(
				Content.title), page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
	elif content_type == 'failed':
		entries = db.paginate(db.select(Content).filter_by(failed=1).order_by(
			Content.title), page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
		if 'date' in request.args:
			entries = db.paginate(db.select(Content).filter_by(failed=1).filter(
				Content.created_at >= request.args.get('date')).order_by(Content.title),
				page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
		elif 'search' in request.args:
			entries = db.paginate(db.select(Content).filter_by(failed=1).filter(
				Content.title.like("%" + request.args.get('search') + "%")).order_by(
				Content.title), page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
	else:
		entries = db.paginate(db.select(Content).filter_by(downloaded=1).filter_by(type=content_type[:-1]
			).order_by(Content.title), page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
		if 'date' in request.args:
			entries = db.paginate(db.select(Content).filter_by(downloaded=1).filter_by(
				type=content_type[:-1]).filter(Content.created_at>=request.args.get('date')).order_by(
				Content.title), page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
		elif 'search' in request.args:
			entries = db.paginate(db.select(Content).filter_by(downloaded=1).filter_by(
				type=content_type[:-1]).filter(Content.title.like("%"+request.args.get('search')+"%")).order_by(
				Content.title), page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
	return render_template('content.html', content_type=content_type, entries=entries, search_by_date_form=search_by_date_form, search_form=search_form)

@app.route('/upload', methods=['GET', 'POST'])
@admin_only
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		uploaded_file = request.files['file']
		if form.type.data == 'movie':
			file_path = ''.join((app.config['PATH_FOR_MOVIES'], uploaded_file.filename))
		elif form.type.data == 'show':
			file_path = ''.join((app.config['PATH_FOR_SHOWS'], uploaded_file.filename))
		uploaded_file.save(file_path)
		content = Content(title=form.name.data, type=form.type.data, description=form.description.data, file_path=file_path)
		db.session.add(content)
		db.session.commit()
		#data = {'content': f'New item uploaded: {form.type.data} - {form.name.data}', 'username': 'AudioVault Notification Bot'}
		#result = requests.post(app.config['DISCORD_URL'], json=data)
		return redirect(url_for('index'))
	return render_template('upload.html', form=form)

@app.route('/generate_description', methods=['POST'])
def generate_description():
	description = get_description(request.form['title'])
	return jsonify({'description': description})

@app.route('/download/<id>')
@login_required
def download(id):
	file_path = db.session.scalar(db.select(Content.file_path).filter_by(id=id))
	return send_file(file_path, as_attachment=True)

@app.route('/delete/<id>', methods=['GET', 'POST'])
@admin_only
def delete(id):
	form = DeleteForm()
	name = db.session.scalar(db.select(Content.title).filter_by(id=id))
	if form.yes.data:
		deleted_item = db.session.get(Content, id)
		db.session.delete(deleted_item)
		db.session.commit()
		if deleted_item.file_path is not None:
			rm(deleted_item.file_path)
		return redirect(url_for('index'))
	elif form.no.data:
		return redirect(url_for('index'))
	return render_template('delete.html', form=form, name=name)

@app.route('/edit/<id>', methods=['GET', 'POST'])
@admin_only
def edit(id):
	item = db.session.get(Content, id)
	form = EditForm(obj=item)
	if form.validate_on_submit():
		if item.file_path != form.file_path.data:
			move(item.file_path, form.file_path.data)
		db.session.execute(db.update(Content), [{'id': id,
			'title': form.title.data, 'type': form.type.data, 'description': form.description.data,
			'file_path': form.file_path.data, 'updated_at': datetime.now(timezone.utc)}])
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('edit.html', form=form)

@app.route('/add_to_featured', methods=['POST'])
@admin_only
def add_to_featured():
	try:
		featured = Featured(content=db.session.get(Content, request.form['id']))
		db.session.add(featured)
		db.session.commit()
		message = 'Added to featured'
	except:
		message = 'Already in featured'
	return jsonify({'message': message})

@app.route('/remove_featured', methods=['POST'])
@admin_only
def remove_featured():
	removed_item = db.session.get(Featured, request.form['id'])
	db.session.delete(removed_item)
	db.session.commit()
	return ''

@app.route('/clear_featured', methods=['POST'])
@admin_only
def clear_featured():
	db.session.execute(db.delete(Featured))
	db.session.commit()
	return ''

@app.route('/add_news', methods=['GET', 'POST'])
@admin_only
def add_news():
	form = AddNewsForm()
	if form.validate_on_submit():
		news = News(content=form.content.data)
		db.session.add(news)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('add_news.html', form=form)

@app.route('/modify_news/<id>', methods=['GET', 'POST'])
@admin_only
def modify_news(id):
	item = db.session.get(News, id)
	form = ModifyNewsForm(obj=item)
	if form.validate_on_submit():
		db.session.execute(db.update(News), [{'id': id, 'content': form.content.data}])
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('edit.html', form=form)

@app.route('/remove_news', methods=['POST'])
@admin_only
def remove_news():
	removed_item = db.session.get(News, request.form['id'])
	db.session.delete(removed_item)
	db.session.commit()
	return ''
