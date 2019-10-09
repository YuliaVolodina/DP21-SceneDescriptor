import werkzeug
from sqlalchemy.exc import DatabaseError
from typing import Optional

from src.domain.models import Image
from src.domain.models import Rating
from src.extensions import db
from src.urate import utils


def create_image(payload: dict):
	path = payload.get('path')
	caption = payload.get('caption')

	image = Image(path=path, caption=caption)

	image.add()
	db.session.commit()

	return image


def get_image(image_id: Optional[str] = None):
	if image_id:
		images = Image.query.get(image_id)
	else:
		images = Image.query.all()

	return images


def update_image(image_id, payload):
	image = Image.query.get(image_id)

	if not image:
		return None

	for k, v in payload.items():
		setattr(image, k, v)

	db.session.commit()

	return image


def delete_image(image_id):
	image = Image.query.get(image_id)

	if not image:
		raise werkzeug.exceptions.NotFound

	try:
		image.delete()
		db.session.commit()
	except Exception:
		db.session.rollback()
		raise DatabaseError


def create_rating(payload):
	user_id = payload.get('user_id')
	image_id = payload.get('image_id')
	validity = payload.get('validity')
	minimalist = payload.get('minimalist')
	distinct_items = payload.get('distinct_items')
	details = payload.get('details')
	spatial_info = payload.get('spatial_info')

	if utils.rating_check(validity) and \
		utils.rating_check(minimalist) and \
		utils.rating_check(distinct_items) and \
		utils.rating_check(details) and \
		utils.rating_check(spatial_info):

		rating = Rating(
			user_id=user_id,
			image_id=image_id,
			validity=validity,
			minimalist=minimalist,
			distinct_items=distinct_items,
			details=details,
			spatial_info=spatial_info
		)

		rating.add()
		db.session.commit()

		return rating
	else:
		return None


def get_rating(image_id: Optional[str] = None, user_id: Optional[str] = None):
	if image_id and user_id:
		ratings = Rating.query.get((user_id, image_id))
	elif image_id:
		ratings = Rating.query.filter(Rating.image_id == image_id)
	elif user_id:
		ratings = Rating.query.filter(Rating.user_id == user_id)
	else:
		raise Exception

	if ratings.first():
		return ratings.all()
	else:
		return None


def update_rating(image_id, user_id, payload):
	rating = Rating.query.get((user_id, image_id))

	if not rating:
		return None

	for k, v in payload.items():
		setattr(rating, k, v)

	db.session.commit()

	return rating


def delete_rating(image_id, user_id):
	rating = Rating.query.get((user_id, image_id))

	if not rating:
		raise werkzeug.exceptions.NotFound

	try:
		rating.delete()
		db.session.commit()
	except Exception:
		db.session.rollback()
		raise DatabaseError
