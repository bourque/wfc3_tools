#! /usr/bin/env python
'''
ABOUT:
Checks to see if the last date entry for each table in ql_log.db is today.
If it is not, updates the table with ID, date, and '-1' values for each
column for each date between the last date logged and today.

AUTHOR:
Matthew Bourque
Space Telescope Science Institute
bourque@stsci.edu

LAST UPDATED:
11/12/12 (Bourque)
'''

import sqlite3
from datetime import datetime
from datetime import timedelta

# -----------------------------------------------------------------------------
# The main controller
# -----------------------------------------------------------------------------

def check_ql_log():
    '''
    The main controller.
    '''

    database = '/grp/hst/wfc3a/Database/ql_log.db'
    tables = ['missing', 'wfc3a_disk_use', 'wfc3b_disk_use',
              'wfc3c_disk_use', 'wfc3d_disk_use', 'wfc3e_disk_use',
              'wfc3f_disk_use', 'wfc3g_disk_use']

    # Open database connection
    conn = sqlite3.connect(database)
    conn.text_factory = str
    db_cursor = conn.cursor()

    for table in tables:

        last_date = get_last_date(db_cursor, table)
        columns, values = get_column_names(db_cursor, table)
        date_list = dates_to_insert(last_date)

        # Insert "-1" for each date between last_date and today
        for date in date_list:
            insert_command = 'INSERT INTO ' + table + '(date, ' + columns + \
                             ') VALUES ("' + date + '", ' + values + ')'
            print insert_command

            db_cursor.execute(insert_command)
            conn.commit()

    # Close database connection
    conn.close()

# -----------------------------------------------------------------------------

def dates_to_insert(last_date):
    '''
    Determines the dates that need to be inserted into ql_log.db.
    '''

    today = datetime.today().strftime('%Y %m %d')
    next_date = last_date
    date_list = []
    while next_date < today:
        next_date = datetime.strftime(datetime.strptime(next_date, 
                    '%Y %m %d') + timedelta(1), '%Y %m %d')
        date_list.append(next_date)

    return date_list

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

def get_last_date(db_cursor, table):
    '''
    Returns the last date entry in the table.
    '''

    date_query = 'SELECT max(date) FROM ' + table
    db_cursor.execute(date_query)
    last_date = db_cursor.fetchall()[0][0]

    return last_date

# -----------------------------------------------------------------------------
# For command line execution
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    check_ql_log()