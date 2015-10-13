import datetime
import psycopg2

#### NOTES #####
# When fetching labels, timestamps are in seconds while for probe data timestamps are in miliseconds.
################

def fetch_data(database, subject_id, table_name, column_names, timestamp_column_name, start=0.0, end=0.0, filter=False, server_address='', username='sosata', password='123'):

    db_string = 'host=\''+server_address+'\' dbname=\'' + database + '\' user=\'' + username + '\' password=\'' + password + '\''
    #print db_string
    conn = psycopg2.connect(db_string)
    cursor = conn.cursor()
    values = []
    column_names = column_names.split(',')
    column_strings = ''

    timestamp_column_name_split = timestamp_column_name.split('.')

    for column_name in column_names:
        if len(column_strings) > 0:
            column_strings += ','
        if len(timestamp_column_name_split)>1:
            column_strings += table_name + '.'
        column_strings += column_name

    if len(timestamp_column_name_split)==1:
        query = 'SELECT ' + timestamp_column_name + ',' + column_strings + ' FROM ' + table_name
        query +=  ' WHERE (' + timestamp_column_name + ' >= %s AND ' + timestamp_column_name + ' <= %s'
        query += ' AND user_id = %s'
        query += ' )'
        query += ' ORDER BY ' + timestamp_column_name + ' ASC'
        query += ';'
    else:
        query = 'SELECT ' + timestamp_column_name + ',' + column_strings + ' FROM ' + table_name + ', ' + timestamp_column_name_split[0]
        query +=  ' WHERE (' + timestamp_column_name + ' >= %s AND ' + timestamp_column_name + ' <= %s'
        query += ' AND ' + table_name + '.user_id = %s AND ' + timestamp_column_name_split[0] + '.id = ' + table_name + '.reading_id'
        query += ' )'
        query += ' ORDER BY ' + timestamp_column_name + ' ASC'
        query += ';'

    #print query

    try:
        #print str((float(start), float(end), subject_id,))
        cursor.execute(query, (float(start), float(end), subject_id,))
        last_saved = datetime.datetime.max
        for result in cursor:
            if filter:
                if len(result) > 1 and result[1] != None and str(result[1]).strip() != '':
                    delta = last_saved - result[0]
                    if delta.days > 0 or delta.seconds > 300:
                        values.append(list(result))
                        last_saved = result[0]
            else:
                if len(result) > 1:
                    if result[1] != None and str(result[1]).strip() != '':
                    	values.append(list(result))
                else:
                    values.append([0, result[0]])
        conn.close()
        cursor.close()
        return values
    except:
        print('\033[91m'+'FetchData: Relation '+table_name+' or some of its columns do not exist.'+'\033[0m')
        return values
