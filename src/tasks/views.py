import redis
from rq import Queue, Connection

from flask import Blueprint
from flask import jsonify
from flask import request

from src.auth.views import token_required
from src.config import Config
from src.tasks import controller

blueprint = Blueprint('tasks', __name__, url_prefix='/tasks')


@blueprint.route('', methods=['POST'])
@token_required
def run_task(current_user):
	task_type = request.get('type', 0)
	with Connection(redis.from_url(Config.REDIS_URL)):
		q = Queue()
		task = q.enqueue(controller.create_task, task_type)

	response_object = {
		'status': 'success',
		'data': {
			'task_id': task.get_id()
		}
	}
	return jsonify(response_object)


@blueprint.route('/<task_id>', methods=['GET'])
@token_required
def get_status(current_user, task_id):
	with Connection(redis.from_url(Config.REDIS_URL)):
		q = Queue()
		task = q.fetch_job(task_id)
	if task:
		response_object = {
			'status': 'success',
			'data': {
				'task_id': task.get_id(),
				'task_status': task.get_status(),
				'task_result': task.result
			}
		}
	else:
		response_object = {'status': 'error'}
	return jsonify(response_object)
