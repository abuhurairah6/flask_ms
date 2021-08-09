import sys
import io
import os
import tempfile
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import json
import base64
import zipfile
from mservice.pictures import upload, download

def test_upload(client):
	data = {}
	data['file'] = (io.BytesIO(b"abcdef"), 'test.jpg')
	response = client.post('/pictures/save', data = data, content_type = 'multipart/form-data')
	response = response.data.decode('utf8')
	response = json.loads(response)
	assert response["status"] == 1
	assert "Successfully uploaded jpg file" in response["msg"]

def test_upload_zip(client):
	filefd, filepath = tempfile.mkstemp()
	zip_object = zipfile.ZipFile(filepath + "temp.zip", "w", zipfile.ZIP_DEFLATED)
	for x in range(1):
		zip_object.writestr("test.jpg", io.BytesIO(b"abcdef").getvalue())
	zip_object.close()
	zip_object = open(filepath + "temp.zip", "rb")
	data = {}
	data['file'] = zip_object
	response = client.post('/pictures/save', data = data, content_type = 'multipart/form-data')
	response = response.data.decode('utf8')
	response = json.loads(response)
	os.close(filefd)
	os.unlink(filepath)
	assert response["status"] == 1
	assert "Successfully uploaded zip file" in response["msg"]

def test_upload_disallowed_extension(client):
	data = {}
	data['file'] = (io.BytesIO(b"abcdef"), 'test.txt')
	response = client.post('/pictures/save', data = data, content_type = 'multipart/form-data')
	response = response.data.decode('utf8')
	response = json.loads(response)
	assert response["status"] == 0
	assert "File extension not allowed" in response["msg"]

def test_download(client):
	response = client.get('/pictures/load?')
	assert b"Please pass a reference link" in response.data

	response = client.get('/pictures/load?link=notvalid')
	assert b"does not exists" in response.data

	response = client.get('/pictures/load?link=TESTLINK')
	file_decode = base64.b64decode("TESTFILEBODY")
	assert response.data == file_decode