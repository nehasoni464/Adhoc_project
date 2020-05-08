import docker
from flask import request, render_template, Blueprint
from apis.authentication.auth import token_required, decode_token
from apis.db.mongo import Database
import datetime

bp = Blueprint('docker', __name__, url_prefix='/docker')


@bp.route('/engine/add', methods=['GET', 'POST'])
@token_required
def add_docker_engine():
	token_data = decode_token()
	db = Database()
	mongo = db.dockerhost
	if request.method == 'POST':
		dockerhost = request.form['dockerhost']

		data = {
			"user" : token_data.get('username'),
			"DOCKER_HOST" : dockerhost.strip(),
			"createdAt" : datetime.datetime.utcnow()
		}

		mongo.insert(data)
		# return f"Dockerhost added {dockerhost}"

	docker_host = mongo.find({"user":token_data.get('username')})
	host = [i.get('DOCKER_HOST') for i in docker_host]

	return render_template('dockerEngine.html', host=host)