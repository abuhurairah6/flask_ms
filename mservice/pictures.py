import base64
import random
from flask import Blueprint, request, send_file, jsonify, make_response
from mservice.db import db_open

bp = Blueprint("pictures", __name__, url_prefix = "/pictures")

@bp.route("/save", methods = ["POST"])
def upload():
	if not request.files['file']:
		return {
			"status": 0,
			"msg": "Please attach a valid attachment"
		}

	file = request.files['file']
	file_encode = base64.b64encode(file.read())
	hash = random.getrandbits(128)
	link = str("%032x" % hash)

	db = db_open()
	db.execute(
		"INSERT INTO PICTURES (P_LINK, P_SOURCE) VALUES (?, ?)",
		(link, file_encode)
	)

	db_cnt = db.execute(
		"SELECT COUNT(*) FROM PICTURES"
	).fetchone()

	db.commit()
	
	msg = "Successfully uploaded. Your reference link is: " + link

	return {
		"status": 1,
		"msg": msg
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