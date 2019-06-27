from flask import Flask

from src import auth
from src.config import Config
from src.domain.models import user_datastore
from src.extensions import db
from src.extensions import migrate
from src.extensions import security


def create_app():
	app = Flask(__name__)

	app.config.from_object(Config())

	register_blueprints(app)
	register_extension(app)

	return app


def register_blueprints(app):
	app.register_blueprint(auth.views.blueprint)


def register_extension(app):
	db.init_app(app)
	migrate.init_app(app, db)
	security.init_app(app, user_datastore)
