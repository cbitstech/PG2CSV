import datetime
from copy import deepcopy
import csv
import os
import sys
import shutil

from fetch_data import fetch_data

def pg2csv(database, subject_id, subject_id_hashed, data_root_dir, probe_info, runtype, server_address, usr, pwd, time_start, time_end):

    #with open(subjects_info) as csvfile:
    #    subject_info = csv.reader(csvfile, delimiter=';', quotechar='|')
    #    for row in subject_info:
    #        if len(row)==2:
    #            if row[0]==subject:
    #                subject_id = row[1]
    #                #year_start = int(row[2])
    #                #month_start = int(row[3])
    #                #day_start = int(row[4])
    #                #hour_start = int(row[5])
    #                #minute_start = int(row[6])
    #                #year_end = int(row[7])
    #                #month_end = int(row[8])
    #                #day_end = int(row[9])
    #                #hour_end = int(row[10])
    #                #minute_end = int(row[11])
    #        else:
    #            subject_id = subject
    #            print subject_id

    #Directory to put the extracted data in:
    dirname = data_root_dir+subject_id
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
        os.makedirs(dirname)
    else:
        os.makedirs(dirname)

    #Set roughly the start and the end of the data timestamps
    #start_all = datetime.datetime(year_start,month_start,day_start,hour_start,minute_start,0)
    #end_all = datetime.datetime(year_end,month_end,day_end,hour_end,minute_end,59)

    #Convert to unix timestamp (seconds):
    #start_all_ts = start_all.strftime('%s')
    #end_all_ts = end_all.strftime('%s')
    import time
    start_all_ts = time.mktime(time_start.timetuple())
    end_all_ts = time.mktime(time_end.timetuple())

    #Reading probes info
    probes = []
    with open(probe_info) as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            if row[0]=='1':
                probes.append(row[1:len(row)])

    # Extractng timestamps for data samples:
    # 'start': timestamps for the start of each trial (x: class; y: trial number)
    # 'end': timestamps for the end of each trial (x: class; y: trial number)
    # Numbers are stored in miliseconds here since the sensor timestamps are in ms.

    if runtype=='trial':
        triggers = fetch_data(database, subject_id_hashed, 'ActivityLog', 'FEATURE_VALUE', 'timestamp', start_all_ts, end_all_ts, False, server_address, usr, pwd)
        start = []
        end = []
        for row in triggers:
            if row[1]=='start':
                start.append(row[0])
            elif row[1]=='end':
                end.append(row[0])
        if len(start)!=len(end):
            print('Start and End triggers are inconsistent!')
            sys.exit(1)
    elif runtype=='all':
        start =  [float(start_all_ts)]
        end =  [float(end_all_ts)]
    else:
        print('Unknown Runtype '+runtype+'!')
        sys.exit(1)


    print
    with open('log_python.txt','a') as logfile:
        logfile.write('\n')
    logfile.close()

    # cut-off time in miliseconds at the beginning and the end
    clip_begin = 0
    clip_end = 0

    num_trials = len(start)

    for probe in probes:
        duplicate_timestamps = 0
        empty_entry = 0
        for j in range(num_trials):
            data = []
            #Setting the start and end timestamps for each trial
            t1 = start[j]+clip_begin
            t2 = end[j]-clip_end
            #Converting t1 and t2 to secs for the probes that have their timestamps in secs
            if probe[4]=='ms':
                t1 = float(t1*1000.0)
                t2 = float(t2*1000.0)
            #Converting t1 and t2 to secs for the probes that have their timestamps in nanosecs
            if probe[4]=='ns':
                t1 = float(t1*1000000000.0)
                t2 = float(t2*1000000000.0)
            #print(probe)
            data_temp = fetch_data(database, subject_id_hashed, probe[0], probe[2], probe[3], t1, t2, False, server_address, usr, pwd)
            if not data_temp:
                #print('\033[93m'+'PG2CSV: There is no data for probe \''+ probe[1] + '\'' + '\033[0m')
                msg = 'Subject '+subject_id+': There is no data for probe \''+ probe[1] + '\''
                print(msg)
                with open('log_python.txt','a') as logfile:
                    logfile.write(msg + '\n')
                logfile.close()
                continue
            num_columns = len(data_temp[0])
            for k in range(len(data_temp)):
                #The first column is the timestamp
                if probe[4]=='s':
                    time = float('%.6f'%(deepcopy(data_temp[k][0])))
                elif probe[4]=='ms':
                    time = float('%.6f'%(deepcopy(data_temp[k][0])/1000.0))
                else:
                    time = float('%.6f'%(deepcopy(data_temp[k][0])/1000000000.0))
                #Saving data sample only when it's different from the previous sample - this is a PR/PostgreSQL communication bug
                if not(len(data)==0) and time==data[len(data)-1][0] and probe[5]=='R':
                    duplicate_timestamps = duplicate_timestamps+1
                if len(data)==0 or time!=data[len(data)-1][0] or probe[5]=='N':
                    data_row = [time]
                    for kk in range(num_columns-1):
                        if not str(data_temp[k][kk+1]):
                            data_row.append('-99')
                            empty_entry = empty_entry+1
                        else:
                            data_row.append(deepcopy(data_temp[k][kk+1]))
                    #data_row.append(class_label)
                    #data_row.append(location_label)
                    data.append(data_row)
            if empty_entry>0:
                msg = 'Subject '+subject_id+': '+str(empty_entry)+' empty entries for probe \''+probe[1]+'\' replaced with \'-99\''
                print(msg)
                with open('log_python.txt','a') as logfile:
                    logfile.write(msg + '\n')
                logfile.close()
            if duplicate_timestamps>0:
                msg = 'Subject '+subject_id+': '+str(duplicate_timestamps)+'/'+str(len(data_temp))+' duplicate timestamps for probe \''+probe[1]+'\' removed'
                print(msg)
                with open('log_python.txt','a') as logfile:
                    logfile.write(msg + '\n')
                logfile.close()
            #Dumping the gathered samples
            if runtype=='trial':
                filename = dirname+'/'+probe[1]+'_trial%d.csv'%(j)
            else:
                filename = dirname+'/'+probe[1]+'.csv'
            with open(filename,'w') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter='\t',quotechar='|',quoting=csv.QUOTE_MINIMAL)
                for i in range(len(data)):
                    spamwriter.writerow(data[i])
