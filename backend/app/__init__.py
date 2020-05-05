from flask import Flask
from flask_cors import CORS


def create_app():
	app = Flask(__name__)
	CORS(app)
	from apis.authentication import auth
	from apis.authentication.auth import token_required
	app.register_blueprint(auth.bp)

	
	@app.route('/')
	@token_required
	def index():
		return "hello world"

	return app
