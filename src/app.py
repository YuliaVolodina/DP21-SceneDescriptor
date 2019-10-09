import redis
from rq import Connection, Worker

from flask import Flask

from src import auth
from src import tasks
from src import urate
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

	@app.cli.command('run_worker')
	def run_worker():
		redis_url = app.config['REDIS_URL']
		redis_connection = redis.from_url(redis_url)
		with Connection(redis_connection):
			worker = Worker(app.config['QUEUES'])
			worker.work()

	return app


def register_blueprints(app):
	app.register_blueprint(auth.views.blueprint)
	app.register_blueprint(tasks.views.blueprint)
	app.register_blueprint(urate.views.blueprint)


def register_extension(app):
	db.init_app(app)
	migrate.init_app(app, db)
	security.init_app(app, user_datastore)
