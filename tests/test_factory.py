import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from mservice import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing