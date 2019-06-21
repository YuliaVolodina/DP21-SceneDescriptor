from flask_security.utils import hash_password
from flask_security.utils import login_user
from flask_security.utils import logout_user
from flask_security.utils import verify_password

from src.domain.models import User
from src.extensions import db
from src.auth.utils import user_to_dict


def register(body: dict) -> dict:
	email = body['email']
	password = hash_password(body['password'])

	if _is_user(email):
		raise Exception
	else:
		user = User(
			email=email,
			password=password)
		user.add()
	db.session.commit()

	return user_to_dict(user)


def login(body: dict):
	email = body['email']
	password = body['password']
	user = User.query.filter(User.email == email).first()
	verified = verify_password(password, user.password)
	if verified:
		auth_token = user.encode_auth_token(user.id)
		if auth_token:
			login_user(user)
			response = {
				'status': 'success',
				'message': 'Successfully logged in.',
				'auth_token': auth_token.decode(),
				'user': user
			}
			db.session.commit()

			return response

	raise Exception


def logout():
	return logout_user()


def get_user_by_id(user_id: int) -> User:
	user = User.query.filter(User.id == user_id).first()
	if user:
		return user
	else:
		raise Exception


def _is_user(email: str) -> bool:
	user = User.query.filter(User.email == email).first()

	return True if user else False
