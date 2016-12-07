##Instructions for using the PG2CSV package

This package queries Purple Robot data from a PostgreSQL server and writes it into tab-separated values (TSV) files.

###Requirements

Before running the scripts make sure you have the following packages installed:

* Python 2.7.6 or higher

* Psycopg 2 or higher - This package enables Python to connect to a PostgreSQL Server. Download it from here:
http://initd.org/psycopg/download/

###Setting the parameters

Set the parameters inside the *main.py* file. 

* You will need a server address and database name to access the database. These will be set by the following variables:
```python
server_address = '<SERVER ADDRESS>'
database = '<DATABASE NAME>'
```

* Set the location for the queried data to be stored:

```python
data_root_dir = '<DATA DIR>'
```

* Determine which subjects and what dates/times you are querying. You need to create a file containing informaion on the subjects actual and hashed IDs, and then set it in *main.py*:

```python
subjects_info = '<SUBJECT INFO FILE>'
```
	
This will be a tab-separated file with the following columns:

**Column 1**: Subject ID - This is arbitrary and will be used as the name of the folder containing each subject's data.

**Column 2**: Database name - This is an MD5 Hash format of the subject's email address, which is used as the name of their database.

<!-- Columns 3-5: Date (yyyy-mm-dd) - the start date 
Columns 6-7: Time (HH:mm) - the start time (the hour is in 24-hour format).
Columns 8-10: Date (yyyy-mm-dd) - the end date 
Columns 11-12: Time (HH:mm) - the end time (the hour is in 24-hour format).
 -->

* Determine which probes you are querying in another tab-separated values (TSV) file, with the following columns:

**Column 1**: Probe name - This is the name which assigned by Purple Robot and used in the database for each probe.

**Column 2**: Probe file name (xxx) - This is an arbitrary, 3-letter name. It will be used as the TSV file name to which Purple Robot data will be written. Make sure each probe has a unique file name.

**Column 3**: Attribute names, in the following format:
```python
<ATTRIBUTE 1>,<ATTRIBUTE 2>,...,<ATTRIBUTE N>
```
 These are the attributes of a probe that you want to query from. For example, for the GPS location probe, you might use 'latitude,longitude' as attributes.

**Column 4**: Timestamp source: This determines the name of the table in the database that will be used as the source of timestamps. These timestamps will be written to TSV files as well. For most probes, this is just *timestamp*. However, for some physical sensor probes, it is *EVENT_TIMESTAMP*. Check Purple Robot documentation for details.

**Column 5**: Timestamp unit (*s* | *ms*): This is the timestamp unit that Purple Robot has used for each probe. Enter *s* for seconds and *ms* for miliseconds.

**Column 6**: Remove duplicates (*R* | *N*): Option to remove data points that have the identical timestamps. *R*: remove; *N*: do not remove. If *R* is chosen, only the first data point out of data points with identical timestamps will be saved.

These information should be written to a file and refered to as the following in *main.py*:

```python
probe_info = '<PROBE INFO FILE>'
```
An example is given in *probes_info.csv*.

5. Set the output directory:

Set where the data is going to be written in *main.py*:

```python
data_root_dir = '<DATA DIR>'
```

###Running the script

```python
python main.py
```

You will be prompted for a username and password. These are *database* credentials, and will be provided to you by the database server administrators.
