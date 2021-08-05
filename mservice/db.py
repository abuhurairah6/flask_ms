import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def app_init(app):
	app.teardown_appcontext(db_close)
	app.cli.add_command(db_init_command)

def db_init():
	db = db_open()

	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

@click.command('db-init')
@with_appcontext
def db_init_command():
	db_init()
	click.echo('Database initialized')

def db_open():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types = sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db

def db_close(e = None):
	db = g.pop('db', None)

	if db is not None:
		db.close()