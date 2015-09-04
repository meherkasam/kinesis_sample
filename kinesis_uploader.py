import constants
import json

class KinesisUploader:
	_client = {}
	def __init__(self, client):
		self._client = client
		
	def upload(self, data_rows):
		# TODO: Start this on a different thread
		for row in data_rows:
			response = self._client.put_record(StreamName=constants.KINESIS_STREAM_NAME, Data=json.dumps(row), PartitionKey="SamplePartition")
			#print response if you want to see output from AWS