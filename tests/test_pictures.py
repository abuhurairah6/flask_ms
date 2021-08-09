import sys
import io
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import json
import base64
from mservice.pictures import upload, download

def test_upload(client):
	data = {}
	data['file'] = (io.BytesIO(b"abcdef"), 'test.jpg')
	response = client.post('/pictures/save', data = data, content_type = 'multipart/form-data')
	response = response.data.decode('utf8')
	response = json.loads(response)
	assert response["status"] == 1

def test_download(client):
	response = client.get('/pictures/load?')
	assert b"Please pass a reference link" in response.data

	response = client.get('/pictures/load?link=notvalid')
	assert b"does not exists" in response.data

	response = client.get('/pictures/load?link=TESTLINK')
	file_decode = base64.b64decode("TESTFILEBODY")
	assert response.data == file_decode