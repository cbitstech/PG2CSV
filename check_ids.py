# This script checks whether dashboard IDs exist in hardware.json and finds the matches.

import json
import csv

info_in = 'dashboard2.csv'
info_out = 'subject_info_cs120_extended2.csv'

with open('hardware.json') as f:
	mapping = json.load(f)
f.close()

with open(info_in) as f:
	subjects = csv.reader(f, delimiter='\t', quotechar='|')
	subjects_new = []
	for subject in subjects:
		found = 0
		ids_hashed = []
		for key, value in mapping.items():
			if subject[6] in value:
				for val in value:
					if len(val)==32:
						found = 1
						ids_hashed.append(val)
		if found==0:
			subjects_new.append([subject[0], subject[6]])
		else:
			ids_hashed_uniq = set(ids_hashed)
			for ids in ids_hashed_uniq:
				subjects_new.append([subject[0], ids])
f.close()

#print subjects_new

#subjects_new = set(subjects_new)
#print 'Extended number of subjects:'
#print len(subjects_new)

with open(info_out,'w') as csvout:
	writer = csv.writer(csvout, delimiter='\t', quotechar='|', lineterminator='\n')
	writer.writerows(subjects_new)
#    for row in subjects_new:
#        print row
#        csvout.write(row)
#        csvout.write('\n')
csvout.close()