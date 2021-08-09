import base64
import random
import zipfile
from flask import Blueprint, request, send_file, jsonify, make_response
from mservice.db import db_open
from werkzeug.datastructures import FileStorage

def get_file_extension(filename):
	return filename.rsplit('.', 1)[1].lower()

def process_regular_file(file):
	result = {}
	file_encode = base64.b64encode(file.read())
	hash = random.getrandbits(128)
	link = str("%032x" % hash)

	db = db_open()
	db.execute(
		"INSERT INTO PICTURES (P_LINK, P_FILENAME, P_SOURCE) VALUES (?, ?, ?)",
		(link, file.filename, file_encode)
	)

	db.commit()
	result[file.filename] = link

	return result

def process_zip_file(file):
	links = {}

	with zipfile.ZipFile(file) as zip_object:
		for filename in zip_object.namelist():
			if get_file_extension(filename) in ("png", "jpeg", "jpg", "svg", "webp"):
				curr_file = FileStorage(stream = zip_object.open(filename), filename = filename)
				link = process_regular_file(curr_file)
				links.update(link)

	return links

bp = Blueprint("pictures", __name__, url_prefix = "/pictures")

@bp.route("/save", methods = ["POST"])
def upload():
	if not request.files['file']:
		return {
			"status": 0,
			"msg": "Please attach a valid attachment"
		}

	file = request.files['file']
	file_ext = get_file_extension(file.filename)

	if file_ext in ("zip"):
		links = process_zip_file(file)
		msg = "Successfully uploaded zip file."
	elif file_ext in ("png", "jpeg", "jpg", "svg", "webp"):
		links = process_regular_file(file)
		msg = "Successfully uploaded " + file_ext + " file."
	else:
		return {
			"status": 0,
			"msg": "File extension not allowed"
		}

	return {
		"status": 1,
		"msg": msg,
		"links": links
	}

@bp.route("/load", methods = ["GET"])
def download():
	link = request.args.get("link")
	if link is None:
		return "Please pass a reference link to your picture!"

	db = db_open()

	file = db.execute(
		"SELECT P_SOURCE FROM PICTURES WHERE P_LINK = ?",
		(link,)
	).fetchone()

	if not file:
		return "Supplied reference link " + link + " does not exists!"

	file_decode = base64.b64decode(file[0])

	response = make_response(file_decode)
	response.headers.set('Content-Type', 'image/jpeg')
	response.headers.set('Content-Disposition', 'attachment')
	return response