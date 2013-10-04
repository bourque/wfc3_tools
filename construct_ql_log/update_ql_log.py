import sqlite3

# -----------------------------------------------------------------------------

def update_disk_stat(orig_database, new_database):
    '''
    Updates the disk stat tables in ql_log.db
    '''

    tables = ['wfc3a_disk_use', 'wfc3b_disk_use', 'wfc3c_disk_use',
              'wfc3d_disk_use', 'wfc3e_disk_use', 'wfc3f_disk_use',
              'wfc3g_disk_use']

    for table in tables:
    
        # Get stats from old database
        conn = sqlite3.connect(orig_database)
        conn.text_factory = str
        db_cursor = conn.cursor()
        command = 'SELECT * FROM ' + table
        db_cursor.execute(command)
        results = db_cursor.fetchall()
        conn.close()

        # Open connection to new database
        conn = sqlite3.connect(new_database)
        db_cursor = conn.cursor()

        # Interpret results
        for i in range(len(results)):
            date = results[i][1]
            size = results[i][2]
            used = results[i][3]
            available = results[i][4]

            # Update the new database
            command = 'UPDATE ' + table + ' SET size = ' + str(size) + ',' + \
                       'used = ' + str(used) + ', available = ' + \
                       str(available) + ' WHERE date = "' + str(date) + '"'
            print command

            db_cursor.execute(command)

        # Commit changes and close connection
        conn.commit()
        conn.close()


# -----------------------------------------------------------------------------

def update_missing(orig_database, new_database):
    '''
    Updates the missing table in ql_log.db
    '''

    # Get stats from old database
    conn = sqlite3.connect(orig_database)
    conn.text_factory = str
    db_cursor = conn.cursor()
    command = 'SELECT * FROM missing'
    db_cursor.execute(command)
    results = db_cursor.fetchall()
    conn.close()

    # Open connection to new database
    conn = sqlite3.connect(new_database)
    db_cursor = conn.cursor()

    # Interpret results
    for i in range(len(results)):
        date = results[i][1]
        flt = results[i][2]
        asn = results[i][3]
        drz = results[i][4]
        ima = results[i][5]
        jif = results[i][6]
        jit = results[i][7]
        jpg = results[i][8]
        raw = results[i][9]
        spt = results[i][10]
        trl = results[i][11]
        crj = results[i][12]

        # Update the new database
        command = 'UPDATE missing SET flt = ' + str(flt) + ',' + \
                  'asn = ' + str(asn) + ',' + \
                  'drz = ' + str(drz) + ',' + \
                  'ima = ' + str(ima) + ',' + \
                  'jif = ' + str(jif) + ',' + \
                  'jit = ' + str(jit) + ',' + \
                  'jpg = ' + str(jpg) + ',' + \
                  'raw = ' + str(raw) + ',' + \
                  'spt = ' + str(spt) + ',' + \
                  'trl = ' + str(trl) + ',' + \
                  'crj = ' + str(crj) + ' WHERE date = "' + str(date) + '"'
        print command

        db_cursor.execute(command)

    # Commit changes and close connection
    conn.commit()
    conn.close()

# -----------------------------------------------------------------------------
#   For command line execution
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    orig_database = '/Users/bourque/wfc3/local_software/construct_ql_log/ql_log_orig.db'
    new_database = '/Users/bourque/wfc3/local_software/construct_ql_log/ql_log.db'

    update_missing(orig_database, new_database)
    update_disk_stat(orig_database, new_database)