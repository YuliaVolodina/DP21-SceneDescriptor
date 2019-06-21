from functools import wraps

from flask import Blueprint
from flask import jsonify
from flask import request

from src.auth import controller
from src.domain.models import User

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if 'Authorization' in request.headers:
			token = request.headers['Authorization']
		if not token:
			return jsonify({'message': 'Token is missing'}), 401

		user_id = User.decode_auth_token(token)
		if isinstance(user_id, str):
			return jsonify({'message': user_id}), 401
		else:
			user = controller.get_user_by_id(user_id)

		if not user.confirmed_at:
			return jsonify({'message': 'Account not validated'}), 401

		return f(user, *args, **kwargs)

	return decorated


def response_to_dict(payload):
	return {
		'authentication_token': payload['auth_token'],
		'status': payload['status'],
		'message': payload['message'],
		'id': payload['user'].id,
		'email': payload['user'].email
	}


@blueprint.route('/login', methods=['POST'])
def login():
	body = request.get_json()
	response = controller.login(body=body)

	return jsonify(response_to_dict(response))


@blueprint.route('/register', methods=['POST'])
def register():
	body = request.get_json()
	user = controller.register(body=body)

	return jsonify(user)


@blueprint.route('', methods=['GET'])
def home_page():
	return 'hello'
