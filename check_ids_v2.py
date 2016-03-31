# This script checks whether hardware.json IDs exist in dashboard and finds the matches.

import json
import csv

with open('dashboard2.csv') as f:
	subjects_csv = csv.reader(f, delimiter='\t', quotechar='|')
	subjects_list = list(subjects_csv)
f.close()

subjects = []
for subject_list_row in subjects_list:
	#print subject_list_row[6]
	subjects.append(subject_list_row[6])

with open('hardware.json') as f:
	mapping = json.load(f)
f.close()

subjects_not_found = []
not_found = 0
for key, values in mapping.items():
	for value in values:
		if not(value in subjects):
			#print str(value)+' not found in dashboard'
			subjects_not_found.append(value)
			not_found += 1

#print not_found
subjects_not_found_uniq = set(subjects_not_found)
for subj in subjects_not_found_uniq:
	print subj
#print len(set(subjects_not_found))
