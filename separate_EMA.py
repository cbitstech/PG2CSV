import os
from shutil import copyfile

source = '/Data/CS120/'
destination = '/Data/CS120_EMA/'

files = ['emc','eml','emm','ems']

if not os.path.isdir(destination):
	os.makedirs(destination)

dirs = os.listdir(source)

for dir in dirs:
	for file in files:
		file_in = source+dir+'/'+file+'.csv'
		file_out = destination+dir+'/'+file+'.csv'
		if os.path.isfile(file_in):
			if not os.path.isdir(destination+dir):
				os.makedirs(destination+dir)
			copyfile(file_in, file_out)
