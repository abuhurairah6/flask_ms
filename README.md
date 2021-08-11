# Flask_MS (Microservice)
Flask_MS is a simple microservice created using [Flask](https://flask.palletsprojects.com/en/2.0.x/) framework integrated with [sqlite3](https://www.sqlite.org/index.html) database. 

## Endpoints
Flask_MS currently holds two simple endpoints: 
1. /pictures/save (POST; params = file) - Uploading images into the database. Allowed file extensions are ".png", ".jpeg", ".jpg", ".svg" and ".webp".
2. /pictures/load (GET; params = link, size) - Download image from given link in the database if available. Size is optional argument, if passed, it will generate at most a 128x128 scaled pictures or smaller depending on size argument.

## Installation

Flask_MS can be installed locally by cloning this git repo and running the following:

```sh
git clone https://github.com/abuhurairah6/flask_ms.git flask_ms
cd flask_ms
pip install -e .
```
## Hosting

Running the server can be done using [venv](https://docs.python.org/3/library/venv.html) startup (for development) or using [gunicorn](https://gunicorn.org/) wsgi:
1. Using venv
```sh
cd flask_ms
. venv/bin/activate
export FLASK_APP=mservice
export FLASK_ENV=development
flask db-init
flask run
```
2. Using gunicorn
```sh
cd flask_ms
gunicorn mservice.wsgi:app
```

The app is currently live hosted on heroku at https://flask-ms-19326.herokuapp.com/ for showcasing purposes. Although since it is currently using heroku, the hosted branch is not master and is heroku-deploy branch instead. Due to heroku's [ephemeral filesystem](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem) - this resets your sqlite database during each startup of the app to heroku or once per day.
