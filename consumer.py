import boto3
import threading
import constants
import utils

class StreamMonitor:
	_client = {}
	_interval = 1
	_iterators = []
	
	def monitor(self):
		threading.Timer(self._interval, self.monitor).start()
		new_iterators = []
		for iterator in self._iterators:
			response = self._client.get_records(ShardIterator=iterator, Limit=10000)
			new_iterators.append(response["NextShardIterator"])
			data = [record["Data"] for record in response["Records"]]
			utils.append_output(data, constants.OUTPUT_FILE)
		self._iterators = new_iterators
		
	def __get_shard_iterators(self, stream_description):
		shard_ids = [shard["ShardId"] for shard in stream_description["StreamDescription"]["Shards"]]
		self._iterators = []
		for i in shard_ids:
			self._iterators.append(self.__get_sharditerator_forid(i))
		
	def __get_sharditerator_forid(self, i):
		return self._client.get_shard_iterator(StreamName=constants.KINESIS_STREAM_NAME, ShardId=i, ShardIteratorType='TRIM_HORIZON')["ShardIterator"]
	
	def __init__(self, client, interval):
		self._client = client
		self._interval = interval
		stream_description = client.describe_stream(StreamName=constants.KINESIS_STREAM_NAME, Limit=10000)
		
		self.__get_shard_iterators(stream_description)
		self.monitor()

kinesis_client = boto3.client("kinesis", region_name=constants.REGION)
StreamMonitor(kinesis_client, constants.MONITORING_INTERVAL)
