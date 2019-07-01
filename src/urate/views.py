import werkzeug
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response
from sqlalchemy.exc import DatabaseError

from src.auth.views import token_required
from src.urate import controller
from src.urate import utils

blueprint = Blueprint('urate', __name__, url_prefix='/urate')

# Image api


@blueprint.route('/images', methods=['GET'])
@token_required
def get_images(current_user):
	images = controller.get_image()
	images_dict = [
		utils.image_to_dict(image) for image in images
	]

	return jsonify(images_dict)


@blueprint.route('/images/<int:image_id>', methods=['GET'])
@token_required
def get_image(current_user, image_id):
	image = controller.get_image(image_id)

	if not image:
		raise werkzeug.exceptions.NotFound

	image_dict = utils.image_to_dict(image)

	return jsonify(image_dict)


@blueprint.route('/images/<int:image_id>', methods=['PATCH'])
@token_required
def patch_image(current_user, image_id):
	body = request.get_json()

	image = controller.update_image(image_id, body)

	if not image:
		raise werkzeug.exceptions.NotFound

	image_dict = utils.image_to_dict(image)

	return jsonify(image_dict)


@blueprint.route('/images/<int:image_id>', methods=['DELETE'])
@token_required
def delete_image(current_user, image_id):
	try:
		controller.delete_image(image_id)

		response = Response(None, status=204)
		response.headers.remove('Content-Type')

		return response
	except werkzeug.exceptions.NotFound:
		return jsonify('Not Found'), 404
	except DatabaseError:
		return jsonify('Method Not Allowed'), 405

# Rating api
