import os


class Config:
	RECENTLY_ADDED = int(os.environ.get('RECENTLY_ADDED') or 3)
	ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE') or 3)
	PAGINATION_EDGE = int(os.environ.get('PAGINATION_EDGE') or 2)
	PAGINATION_CURRENT = int(os.environ.get('PAGINATION_CURRENT') or 2)
	PATH_FOR_SHOWS = os.environ.get('PATH_FOR_SHOWS') or "d:\\uploads\\shows\\"
	PATH_FOR_MOVIES = os.environ.get('PATH_FOR_MOVIES') or "d:\\uploads\\movies\\"
	MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 1024 ** 3 * 2)
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
	f"mariadb+mariadbconnector://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@db/{os.environ.get('DB_NAME')}" or \
	'mariadb+mariadbconnector://root:Password123!@localhost/audiovault'
	SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO') or True
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
	MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'audiovault'
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Password123!'
	MAIL_SENDER = os.environ.get('MAIL_SENDER') or 'audiovault@mail.com'
	DISCORD_URL = os.environ.get('DISCORD_URL') or 'https://discordapp.com/api/webhooks/'
	SEND_UPLOAD_NOTIFICATION = os.environ.get('SEND_UPLOAD_NOTIFICATION') or False
