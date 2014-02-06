#! /usr/bin/env python

'''
ABOUT:
This program creates a file containing metadata for the "master column" image.
'''

from astropy.io import ascii
import sqlite3

# -----------------------------------------------------------------------------

def query_for_times(rootname_list):
    '''
    Queries the Quicklook Database and returns a list of DATE-OBSs and
    TIME-OBS for a list of rootnames.
    '''

    print 'Gathering time information.'

    # Open database connection
    conn = sqlite3.connect('/grp/hst/wfc3a/Database/ql.db')
    conn.text_factory = str
    db_cursor = conn.cursor()

    dateobs_list, timeobs_list = [], []

    for rootname in rootname_list:
        
        # Build query
        command = 'SELECT "DATE-OBS", "TIME-OBS" ' + \
                  'FROM UVIS_FLT_0 ' + \
                  'WHERE filename like "{}%"'.format(rootname)
        print command

        # Execute query
        db_cursor.execute(command)

        # Parse results
        results = db_cursor.fetchall()
        assert len(results) > 0, 'Query did not yield any resuts.'
        dateobs_list.extend([result[0] for result in results])
        timeobs_list.extend([result[1] for result in results])

    # Close database connection
    conn.close()

    return dateobs_list, timeobs_list

# -----------------------------------------------------------------------------

def write_metadata(targname, header_data, qldb_rootnames):
    '''
    Writes an output file containing the relationships between the columns,
    rootnames, and times of observation.
    '''

    # Build dictionary containing data to send to output
    out_dict = {}
    out_dict['orig_columns'] = [header_data['col'][i] for i in 
        range(len(header_data)) if header_data['rootname'][i] 
        in qldb_rootnames]
    out_dict['new_columns'] = [i for i in range(len(out_dict['orig_columns']))]
    out_dict['rootnames'] = [header_data['rootname'][i] for i in 
        range(len(header_data)) if header_data['rootname'][i] 
        in qldb_rootnames]

    # Query database for DATE-OBS and TIME-OBS for each rootname
    out_dict['date_obs'], out_dict['time_obs'] = \
        query_for_times(out_dict['rootnames'])

    # Write results to text file
    outfile = '{}_metadata.dat'.format(targname)
    ascii.write([
        out_dict['orig_columns'], 
        out_dict['new_coluns'],
        out_dict['rootnames'], 
        out_dict['date_obs'], 
        out_dict['time_obs']], 
        outfile, 
        names=['orig column', 'new column', 'rootname', 'DATE-OBS', 
               'TIME-OBS'])