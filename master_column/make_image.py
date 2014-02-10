#! /usr/bin/env python

'''
ABOUT:
This object creates an image of all WFC3 on-orbit columns for given TARGNAME
and EXPTIME using Jay Anderson's master fits images.
'''

from astropy.io import ascii
from astropy.io import fits
import numpy as np
import os
import sqlite3

# -----------------------------------------------------------------------------

class MakeImage():
    '''
    Parent class.
    '''

    # -------------------------------------------------------------------------

    def __init__(self, targname, exptime, postflash, master_image, 
                 metadata_switch):
        '''
        Assigns argument variables to class instances.
        '''

        self.targname = targname
        self.exptime = exptime
        self.postflash = postflash
        self.master_image = master_image
        self.metadata_switch = metadata_switch

    # -------------------------------------------------------------------------

    def extract_header_data(self):
        '''
        Extracts header data in header file for rows meeting the TARGNAME and
        EXPTIME criteria
        '''

        header_file = 'raw2raz_AMPC.hdr'
        print 'Reading data from {}.'.format(header_file)

        # Read in header file
        self.header_data = ascii.read(header_file, data_start=0, 
            names=['col', 'nrec', 'rootname', 'imagetype', 'filter', 'exptime', 
                   'ccdgain', 'pa_v3', 'crpix1', 'crpix2', 'crval1', 'crval2', 
                   'cd1_1', 'cd1_2', 'cd2_1', 'cd2_2', 'bark', 'sigk', 
                   'rbiask', 'ibiask', 'loc'])

    # -------------------------------------------------------------------------

    def query_for_rootnames(self):
        '''
        Queries the Quicklook Database and returns a list of rootnames
        meeting the TARGNAME and EXPTIME criteria.
        '''

        # Open database connection
        conn = sqlite3.connect('/grp/hst/wfc3a/Database/ql.db')
        conn.text_factory = str
        db_cursor = conn.cursor()

        # Build query
        command = 'SELECT filename ' + \
                  'FROM UVIS_FLT_0 ' + \
                  'WHERE TARGNAME = "{}" '.format(self.targname) + \
                  'AND EXPTIME = "{}" '.format(self.exptime) + \
                  'AND CHINJECT = "NONE"'

        if self.postflash == 'on':
            command += ' AND FLSHFILE LIKE "iref%"'
        elif self.postflash == 'off':
            command += ' AND FLSHFILE LIKE "N/A"'

        # Execute query
        db_cursor.execute(command)

        # Parse results
        results = db_cursor.fetchall()
        assert len(results) > 0, 'Query did not yield any resuts.'
        self.qldb_rootnames = [result[0].split('_')[0] for result in results]

        # Close database connections
        conn.close()

    # -------------------------------------------------------------------------

    def remove_bad_columns(self):
        '''
        Removes columns that do not contain data of interest by comparing the
        rootnames extracted from the QL database to the those in the header 
        file.
        '''

        print 'Removing unwanted columns'

        # Remove excess columns at the end
        excess_start = len(self.header_data)
        excess_end = self.frame.shape[1]
        excess_cols = range(excess_start, excess_end)
        self.cleaned_frame = np.delete(self.frame, excess_cols, 1)

        # Remove cols from other images
        bad_cols = [
            self.header_data['col'][i] - 1
            for i in range(len(self.header_data)) 
            if self.header_data['rootname'][i] not in self.qldb_rootnames]
        self.cleaned_frame = np.delete(self.cleaned_frame, bad_cols, 1)

    # -------------------------------------------------------------------------

    def read_image(self):
        '''
        Reads in the 'master image'.
        '''

        # Read in FITS image
        print 'Reading in master image.'
        self.frame = fits.open(self.master_image, 
                               ignore_missing_end = True)[0].data

    # -------------------------------------------------------------------------

    def save_image(self, image):
        '''
        Saves the 'master image'.
        '''

        newfile = self.master_image.replace(
            '.fits', '_{}.fits'.format(self.targname))
        fits.writeto(newfile, image, header=None, clobber=True)
        print 'Saved image to {}'.format(newfile)