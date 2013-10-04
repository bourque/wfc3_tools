import sqlite3
import datetime
from datetime import date, timedelta

# -----------------------------------------------------------------------------

def get_column_names(db_cursor, table):
    '''
    Returns a string of column names and a string of "-1"s to use as input.
    '''

    # Get column names from table
    table_query = 'PRAGMA table_info("' + table + '")'
    db_cursor.execute(table_query)
    results = db_cursor.fetchall()
    results = [results[i][1] for i in range(len(results))]
    columns = ', '.join(results[2:])

    # Create string of "-1"s
    values = ', '.join(['-1' for i in results[2:]])

    return columns, values

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    database = '/Users/bourque/wfc3/local_software/construct_ql_log/ql_log.db'
    tables = ['missing', 'wfc3a_disk_use', 'wfc3b_disk_use',
              'wfc3c_disk_use', 'wfc3d_disk_use', 'wfc3e_disk_use',
              'wfc3f_disk_use', 'wfc3g_disk_use', 'wfc3h_disk_use', 
              'wfc3i_disk_use']

    conn = sqlite3.connect(database)
    db_cursor = conn.cursor()

    for table in tables:

        id = 1
        date_entry = date(2011, 7, 6)
        delta = timedelta(days=1)
        end_date = date.today()

        columns, values = get_column_names(db_cursor, table)

        while date_entry <= end_date:

            command = 'INSERT INTO ' + table + ' (id, date, ' + columns + \
                      ') VALUES (' + str(id) + ', "' + \
                      date_entry.strftime('%Y %m %d') + '", ' + values + ')'
            
            date_entry += delta
            id += 1
            print command

            db_cursor.execute(command)
            conn.commit()
        
    conn.close()