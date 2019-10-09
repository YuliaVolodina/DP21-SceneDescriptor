from flask_security.utils import hash_password
from flask_security.utils import login_user
from flask_security.utils import logout_user
from flask_security.utils import verify_password

from src.domain.models import User
from src.domain.models import user_datastore
from src.extensions import db
from src.auth.utils import user_to_dict


def register(body: dict) -> dict:
	email = body.get('email')
	password = hash_password(body.get('password'))
	username = body.get('username')

	if _is_user(email):
		raise Exception
	else:
		user = user_datastore.create_user(
			email=email,
			password=password
		)
	db.session.commit()

	return user_to_dict(user)


def login(body: dict):
	email = body.get('email')
	password = body.get('password')
	user = user_datastore.find_user(email=email)
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
