#! /usr/bin/env python

'''
ABOUT:
This program creates an image of all WFC3 on-orbit columns for given TARGNAME,
EXPTIME, and PROPOSID using Jay Anderson's master fits images.
'''

from astropy.io import ascii
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# -----------------------------------------------------------------------------

class colImage():
    '''
    Parent class.
    '''

    # -------------------------------------------------------------------------

    def __init__(self, targname, exptime):
        '''
        Assigns argument variables to class instances.
        '''

        self.targname = targname
        self.exptime = exptime

    # -------------------------------------------------------------------------

    def extract_header_data(self):
        '''
        Extracts header data in header file for rows meeting the TARGNAME and
        EXPTIME criteria
        '''

        header_file = 'raw2raz_AMPC.hdr'
        print 'Reading data from {}.'.format(header_file)

        # Read in header file
        header_data = ascii.read(header_file, data_start=0, 
            names=['col', 'nrec', 'rootname', 'imagetype', 'filter', 'exptime', 
                   'ccdgain', 'pa_v3', 'crpix1', 'crpix2', 'crval1', 'crval2', 
                   'cd1_1', 'cd1_2', 'cd2_1', 'cd2_2', 'bark', 'sigk', 
                   'rbiask', 'ibiask', 'loc'])

        return header_data

    # -------------------------------------------------------------------------

    def query_qldb(self):
        '''
        Queries the Quicklook Database and returns a list of rootnames meeting
        the TARGNAME and EXPTIME criteria.
        '''

        # Open database connection
        conn = sqlite3.connect('/grp/hst/wfc3a/Database/ql.db')
        conn.text_factory = str
        db_cursor = conn.cursor()

        # Build query
        command = "SELECT filename " + \
                  "FROM UVIS_FLT_0 " + \
                  "WHERE TARGNAME = '{}' ".format(self.targname) + \
                  "AND EXPTIME = '{}'".format(self.exptime)
        print command

        # Execute query
        db_cursor.execute(command)

        # Parse results
        results = db_cursor.fetchall()
        qldb_rootnames = [result[0].split('_')[0] for result in results]

        return qldb_rootnames

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def col_image_main(self):
        '''
        The main controller.
        '''

        # Query Quicklook Database to gather list of rootnames to process
        qldb_rootnames = self.query_qldb()

        # Read in amp header file
        header_data = self.extract_header_data()

        # Determine which columns contain data of interest
        print 'Extracting data of interest.'
        data_cols = [
            header_data['col'][i] 
            for i in range(len(header_data)) 
            if header_data['rootname'][i] in qldb_rootnames]

        # Read in FITS image
        print 'Reading in image.'
        frame = fits.open('AMPC_I0101.fits', ignore_missing_end = True)[0].data

    # -------------------------------------------------------------------------

if __name__ == '__main__':

    col_image = colImage('DARK', '900.0')
    col_image.col_image_main()