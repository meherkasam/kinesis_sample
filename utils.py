import os
import json

def directory_to_set(path, extension):
	files_set = set()
	for f in os.listdir(path):
		if f.endswith(extension):
			files_set.add(path + '/' + f)
	return files_set
	
def read_json(file_path):
	data = []
	with open(file_path) as data_file:
		data = json.load(data_file)
	return data