import getpass
from pg2csv import pg2csv
import datetime
import csv
from copy import deepcopy

time_start = datetime.datetime(2015, 10, 28, 0, 0, 0)
time_end = datetime.datetime(2016, 12, 1, 23, 59, 59)

server_address = '<SERVER ADDRESS>'
database = '<DATABASE NAME>'

data_root_dir = '<DATA DIR>'

subjects_info = '<SUBJECT INFO FILE>'
probe_info = '<PROBE INFO FILE>'


# all:      fetches all data from the start to the end date specified in 'subjects_info.csv'
# trial:    fetches only data between subsequent 'start' and 'end' labels in 'ActivityLog'
runtype = 'all'

usr = raw_input('Username: ')
print 'Username: ' + usr
pwd = getpass.getpass("Password: ")

with open('log_python.txt','w') as logfile:
    logfile.write('');
logfile.close()

with open(subjects_info) as csvfile:
    subject_info = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in subject_info:
    	pg2csv(database, row[1], row[1], data_root_dir, probe_info, runtype, server_address, usr, pwd, time_start, time_end)
csvfile.close()
