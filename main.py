import getpass
from pg2csv import pg2csv
import datetime
import csv
from copy import deepcopy

time_start = datetime.datetime(2015, 10, 28, 0, 0, 0)
time_end = datetime.datetime(2016, 3, 21, 23, 59, 59)

data_root_dir = '/Data/CS120/'

subjects_info = 'subject_info_cs120_extended2.csv'	# note: extended file is in use

probe_info = 'probe_info_cs120.csv'

server_address = '165.124.45.185'   #mac server
#server_address = '192.168.56.101'  #local server
database = 'p20_flat'

# all:      fetches all data from the start to the end date specified in 'subjects_info.csv'
# trial:    fetches only data between subsequent 'start' and 'end' labels in 'ActivityLog'
runtype = 'all'

#usr = raw_input('Username: ')
print 'Username: p20_flat'
usr = 'p20_user'
pwd = getpass.getpass("Password: ")
#pwd = ''

with open('log_python.txt','w') as logfile:
    logfile.write('');
logfile.close()

with open(subjects_info) as csvfile:
    subject_info = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in subject_info:
		pg2csv(database, row[1], row[1], data_root_dir, probe_info, runtype, server_address, usr, pwd, time_start, time_end)
