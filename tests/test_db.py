import sys, os
import pytest
import sqlite3
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from mservice.db import db_open

def test_open_close_db(app):
    with app.app_context():
        db = db_open()
        assert db is db_open()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('mservice.db.db_init', fake_init_db)
    result = runner.invoke(args=['db-init'])
    assert 'initialized' in result.output
    assert Recorder.called