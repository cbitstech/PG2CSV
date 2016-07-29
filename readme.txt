Instructions for using the PG2CSV package
------------------------------------------
August 2015

The PG2CSV package queries Purple Robot data from a PostgreSQL server and writes it into tab-separated CSV files.

1. Prerequisites:

Before running the scripts make sure you have the following packages installed:

Python 2.7.6 or higher

Psychopgs 2 or higher - This package enables Python to connect to a PostgreSQL Server. Download it from here:
http://initd.org/psycopg/download/

2. Set the data server address:

You need to set the data server address in the main.py script file:
server_address = 'your_server_address'

3. Determine which subjects and what dates/times are you querying:

'subject_info.csv' is a tab-separated CSV file containing information about which subjects and what time period for each subject are being queried.

Column 1: Subject ID - This is arbitrary and will be used as the name of the folder containing each subject's data.
Column 2: Database name - This is an MD5 Hash format of the subject's email address, which is used as the name of their database.
Columns 3-5: Date (yyyy-mm-dd) - the start date 
Columns 6-7: Time (HH:mm) - the start time (the hour is in 24-hour format).
Columns 8-10: Date (yyyy-mm-dd) - the end date 
Columns 11-12: Time (HH:mm) - the end time (the hour is in 24-hour format).

4. Determine which probes you are querying:

'probes_info.csv' is a tab-separated CSV file containnig information about which probes and which attributes of each probe are being queried.

Column 1: Probe name - This is the name which assigned by Purple Robot and used in the database for each probe.
Column 2: Probe file name (xxx) - This should be an arbitrary, 3 letters long name. It will be used as the CSV file name in which the data will be written. Make sure each probe has a unique file name.
Column 3: Attribute names (A,B,C,...) - These are the attributes of a probe that you want to query from (for example, you might want the X,Y,Z attributes of the accelerometer probe).
Column 4: Timestamp source: This determines the name of the table in the database that will be used as the source of timestamps (timestamps will be written to CSV files too). For most probes, this is going to be 'timestamp'. For some physical probes, it should be 'EVENT_TIMESTAMP'. Check PR documentation for details.
Column 5: Timestamp unit (s | ms): This is the timestamp unit that PR uses for each probe. Enter 's' for seconds and 'ms' for miliseconds. Check PR documentation for details.
Column 6: Remove duplicates (R | N) - The option to remove datapoints that have the same timestamps. 'R': remove; 'N': do not remove.

5. Set the output directory:

Set where the data is going to be written in the main.py script:
data_root_dir = 'destination_directory'

6. Run the main script:

python main.py

You will be prompted for a username and password, which are the ones you use to connect to the database server.
