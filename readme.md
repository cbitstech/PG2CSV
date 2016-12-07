#Instructions

This package queries Purple Robot data from a PostgreSQL server and writes it into tab-separated values (TSV) files.

###1. Dependencies

Before running the scripts make sure you have the following installed:

* Python 2.7.6 or higher

* Psycopg 2 or higher - This package enables Python to connect to a PostgreSQL server. Installation instructions can be found [here](http://initd.org/psycopg/docs/install.html#installation).

###2. Subject information

Create a TSV file containing the following columns:

**Column 1**: Subject's arbitrary ID - This will be used as the name of the folder containing each subject's data.

**Column 2**: Subject's hashed ID - This is an MD5 hashed version of the subject's Google name, which is used as their name inside the database.

<!-- Columns 3-5: Date (yyyy-mm-dd) - the start date 
Columns 6-7: Time (HH:mm) - the start time (the hour is in 24-hour format).
Columns 8-10: Date (yyyy-mm-dd) - the end date 
Columns 11-12: Time (HH:mm) - the end time (the hour is in 24-hour format).
 -->

###3. Probe information

Create a TSV file that determines which probes are being queried. This file should contain the following columns:

**Column 1**: Probe name - This is the name which is assigned by Purple Robot and used in the database for each probe.

**Column 2**: Probe file name (xxx) - This is an arbitrary, 3-letter name. It will be used as the TSV file name to which Purple Robot data will be written. Make sure each probe has a unique file name.

**Column 3**: Attribute names, in the following format:
```python
<ATTRIBUTE 1>,<ATTRIBUTE 2>,...,<ATTRIBUTE N>
```
 These are the attributes of a probe that you want to query from. For example, for the GPS location probe, you might use *latitude,longitude* as attributes.

**Column 4**: Timestamp source: This determines the name of the table in the database that will be used as the source of timestamps. These timestamps will be written to TSV files as well. For most probes, this is just *timestamp*. However, for some physical sensor probes, it is *EVENT_TIMESTAMP*. Check Purple Robot documentation for details.

**Column 5**: Timestamp unit (*s* | *ms*): This is the timestamp unit that Purple Robot has used for each probe. Enter *s* for seconds and *ms* for miliseconds.

**Column 6**: Remove duplicates (*R* | *N*): Option to remove data points that have the identical timestamps (*R*: remove; *N*: not remove). If *R* is chosen, only the first data point out of the data points with identical timestamps is saved, and the rest are removed.

An example is given in *probes_info.csv*.

###4. Script parameters

Set the following parameters in *main.py*: 

* You will need a server address and database name to access the database. These will be set by the following variables:
```python
server_address = '<SERVER ADDRESS>'
database = '<DATABASE NAME>'
```

* Set the location for the queried data to be stored:

```python
data_root_dir = '<DATA DIR>'
```

* Point to the subject information file:

```python
subjects_info = '<SUBJECT INFO FILE>'
```

* Point to the probe information file.

```python
probe_info = '<PROBE INFO FILE>'
```

* Set the output directory where the data is written:

```python
data_root_dir = '<DATA DIR>'
```

###5. Running the script

Run the Python script:
```python
python main.py
```

You will be prompted for a username and password. These are the database credentials, and will be provided to you by the database server administrators.
