import datetime
import jwt
from flask_security import RoleMixin
from flask_security import Security
from flask_security import SQLAlchemyUserDatastore
from flask_login import UserMixin
from src.extensions import db
from src.domain.base import BaseModel


class Image(BaseModel):
	__tablename__ = 'image'
	id = db.Column(db.Integer(), primary_key=True)
	path = db.Column(db.String(256), nullable=False)
	caption = db.Column(db.String(128), nullable=False)


class Role(BaseModel, RoleMixin):
	__tablename__ = 'role'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))


class User(BaseModel, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(128), index=True, unique=True, nullable=False)
	username = db.Column(db.String(128), index=True, unique=True, nullable=False)
	password = db.Column(db.String(256), nullable=False)
	current_login_at = db.Column(db.DateTime())
	current_login_ip = db.Column(db.String(100))
	login_count = db.Column(db.Integer)

	@staticmethod
	def encode_auth_token(user_id):
		"""
		Generates the Auth Token
		:return: string
		"""
		try:
			payload = {
				'exp':
					datetime.datetime.utcnow() + datetime.timedelta(
						days=0, seconds=3600),
				'iat':
					datetime.datetime.utcnow(),
				'sub':
					user_id,
			}
			return jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
		except Exception as e:
			return e

	@staticmethod
	def decode_auth_token(auth_token):
		"""
		Decodes the auth token
		:param auth_token:
		:return: integer|string
		"""
		try:
			payload = jwt.decode(auth_token, 'SECRET_KEY')
			return payload['sub']
		except jwt.ExpiredSignatureError:
			return 'Signature expired. Please log in again.'
		except jwt.InvalidTokenError:
			return 'Invalid token. Please log in again.'


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)