from flask import Blueprint

from mservice.db import db_open

bp = Blueprint("pictures", __name__, url_prefix = "/pictures")

@bp.route("/save", methods = ["POST"])
def upload():
	db = db_open()
	db_cnt = db.execute(
		"SELECT COUNT(*) res FROM PICTURES"
	).fetchone()
	
	msg = "This is a test response. Total db entries = " + str(db_cnt[0])

	return {
		"status": 1,
		"msg": msg
	}