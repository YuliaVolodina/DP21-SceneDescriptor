import werkzeug
from sqlalchemy.exc import DatabaseError
from typing import Optional

from src.domain.models import Image
from src.extensions import db


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
