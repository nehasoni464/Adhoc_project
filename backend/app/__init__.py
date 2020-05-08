from flask import Flask , render_template, session
from flask_cors import CORS


def create_app():
	app = Flask(__name__,template_folder="../templates")
	app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
	# print(dir(app))
	# print(app.config)
	# input()
	CORS(app)
	from apis.authentication import auth
	from apis.dockerapp import pydocker
	from apis.authentication.auth import token_required
	app.register_blueprint(auth.bp)
	app.register_blueprint(pydocker.bp)

	
	@app.route('/')
	@token_required
	def index():
		return "Hello world"
	return app
