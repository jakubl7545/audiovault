import os


class Config:
	RECENTLY_ADDED = int(os.environ.get('RECENTLY_ADDED', 3))
	ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 3))
	PAGINATION_EDGE = int(os.environ.get('PAGINATION_EDGE', 2))
	PAGINATION_CURRENT = int(os.environ.get('PAGINATION_CURRENT', 2))
	PATH_FOR_SHOWS = os.environ.get('PATH_FOR_SHOWS', 'd:\\uploads\\shows\\')
	PATH_FOR_MOVIES = os.environ.get('PATH_FOR_MOVIES', 'd:\\uploads\\movies\\')
	MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 1024 ** 3 * 2))
	SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
	f"mariadb+mariadbconnector://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@db/{os.environ.get('DB_NAME')}")
	SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', True)
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
	MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 1)
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'audiovault')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'Password123!')
	MAIL_SENDER = os.environ.get('MAIL_SENDER', 'audiovault@mail.com')
	DISCORD_URL = os.environ.get('DISCORD_URL', 'https://discordapp.com/api/webhooks/')
	SEND_UPLOAD_NOTIFICATION = int(os.environ.get('SEND_UPLOAD_NOTIFICATION', 0))
	RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
	RATELIMIT_DOWNLOAD_ENDPOINT = os.environ.get('RATELIMIT_DOWNLOAD_ENDPOINT', '3 per minute')
