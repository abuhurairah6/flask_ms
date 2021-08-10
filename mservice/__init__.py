import os
from flask import Flask

def create_app(environ, start_response, test_config = None):
	app = Flask(__name__, instance_relative_config = True)
	app.config.from_mapping(
		SECRET_KEY = 'DEV',
		DATABASE = os.path.join(app.instance_path, 'db.sqlite')
	)

	if test_config is None:
		app.config.from_pyfile('config.py', silent = True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/')
	def main():
	    appName = __name__
	    return "You are currently browsing " + appName + " api."

	from . import db
	db.app_init(app)

	from . import pictures
	app.register_blueprint(pictures.bp)

	return app