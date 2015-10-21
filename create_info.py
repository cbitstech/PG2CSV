import csv

info_in = 'dashboard.csv'
info_out = 'subject_info_cs120.csv'

with open(info_out,'w') as csvout:
    with open(info_in) as csvin:
        info_in = csv.reader(csvin, delimiter='\t', quotechar='|')
        for row in info_in:
            csvout.write(row[0])
            csvout.write(';')
            csvout.write(row[5])
            csvout.write('\n')
csvout.close()
