import os, sys
import ast

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

import google.protobuf as pf

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "static/api-key.json"

def get_prediction(content):
	prediction_client = automl_v1beta1.PredictionServiceClient()

	name = 'projects/<>/locations/us-central1/models/<>'
	payload = {'image': {'image_bytes': content }}
	params = {}
	request = prediction_client.predict(name, payload, params)

	result_json = ast.literal_eval(pf.json_format.MessageToJson(request, including_default_value_fields=False))
	try:
		prediction = result_json["payload"][0]["displayName"]
	except Exception as e:
		prediction="nothing"

	return prediction

def filepath_to_char(filepath):
	with open (filepath, "rb") as ff:
		content = ff.read()
	return get_prediction(content)

if __name__ == '__main__':

	file_path="static/A297.jpg"

	with open(file_path, 'rb') as ff:
		content = ff.read()

	result = get_prediction(content, project_id, model_id)
	print(result)