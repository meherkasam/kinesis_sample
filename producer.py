import boto3
import constants
import directory_monitor
import kinesis_uploader
import utils
		
def start():
	kinesis_client = boto3.client("kinesis", region_name=constants.REGION)
	uploader = kinesis_uploader.KinesisUploader(kinesis_client)
	directory_monitor.DirectoryMonitor(constants.LOG_PATH, constants.EXTENSION, constants.MONITORING_INTERVAL, uploader)
	
start()