import threading
import kinesis_uploader
import utils

class DirectoryMonitor:
	_directory_path = ""
	_extension = ""
	_interval = 1
	_uploader = {}
	_before_files = []
	
	def monitor(self):
		threading.Timer(self._interval, self.monitor).start()
		after_files = utils.directory_to_set(self._directory_path, self._extension)
		new_files = after_files.difference(self._before_files)
		
		if len(new_files) > 0 :
			for f in new_files :
				data_rows = utils.read_json(f)
				self._uploader.upload(data_rows)
				
		self._before_files = after_files
		
	def __init__(self, path, extension, interval, uploader):
		self._directory_path = path
		self._extension = extension
		self._interval = interval
		self._uploader = uploader
		self.monitor()