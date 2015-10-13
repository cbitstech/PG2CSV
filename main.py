import getpass
from pg2csv import pg2csv
import datetime
import csv

#subjects = ['TEST1','TEST2','TEST3','TEST4','TEST5','TEST6','TEST7']

time_start = datetime.datetime(2015, 10, 3, 0, 0, 0)
time_end = datetime.datetime(2015, 10, 12, 23, 59, 59)

data_root_dir = '/Data/CS120_test/'

subjects_info = 'subject_info_cbits.csv'

probe_info = 'probe_info_cs120.csv'

#server_address = '165.124.45.185'
server_address = '192.168.56.101'
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
    subject_info = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in subject_info:
		pg2csv(database, row[0], data_root_dir, subjects_info, probe_info, runtype, server_address, usr, pwd, time_start, time_end)
