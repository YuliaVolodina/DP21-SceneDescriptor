from src.extensions import db
from src.domain.base import BaseModel


class User(BaseModel):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(128), index=True, unique=True)
	password = db.Column(db.String(256), nullable=False)
