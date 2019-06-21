import os


class Config(object):
	APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
	PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Flask Security settings
	WTF_CSRF_ENABLED = False
	SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
	SECURITY_TRACKABLE = True
	SECURITY_PASSWORD_SALT = 'something_super_secret_change_in_production'
	SECURITY_TOKEN_MAX_AGE = 3600

	@property
	def db_uri_fragments(self):
		db_uri_fragments = []
		for name in [
			'MYSQL_USERNAME',
			'MYSQL_PASSWORD',
			'MYSQL_HOSTNAME',
			'MYSQL_DATABASE',
		]:
			var = os.environ.get(name, None)
			db_uri_fragments.append((var, name))

		return db_uri_fragments

	def check_db_uri_fragments(self):
		"""Raise an Exception if any
		db fragments are unset.
		"""
		for frag, varname in self.db_uri_fragments:
			if frag is None:
				raise Exception(
					"Missing environment variable '{0}'".format(varname))

	@property
	def set_sqlalchemy_database_uri(self):
		try:
			self.check_db_uri_fragments()
		except Exception as e:
			raise e
		return "mysql+pymysql://{0}:{1}@{2}/{3}".format(
			*[e[0] for e in self.db_uri_fragments])

	SQLALCHEMY_DATABASE_URI: str = set_sqlalchemy_database_uri
