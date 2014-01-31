#! /usr/bin/env python

'''
ABOUT:
This program creates an image of all WFC3 on-orbit columns for given TARGNAME,
EXPTIME, and PROPOSID using Jay Anderson's master fits images.
'''

import argparse
from astropy.io import ascii
from astropy.io import fits
import numpy as np
import os
import sqlite3

# -----------------------------------------------------------------------------

class colImage():
    '''
    Parent class.
    '''

    # -------------------------------------------------------------------------

    def __init__(self, targname, exptime, master_image):
        '''
        Assigns argument variables to class instances.
        '''

        self.targname = targname
        self.exptime = exptime
        self.master_image = master_image

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
        assert len(results) > 0, 'Query did not yield any resuts.'
        self.qldb_rootnames = [result[0].split('_')[0] for result in results]

    # -------------------------------------------------------------------------

    def remove_columns(self):
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
            se;f.header_data['col'][i] 
            for i in range(len(self.header_data)) 
            if self.header_data['rootname'][i] not in self.qldb_rootnames]
        self.cleaned_frame = np.delete(self.cleaned_frame, bad_cols, 1)

    # -------------------------------------------------------------------------

    def read_image():
        '''
        Reads in the 'master image'.
        '''

        # Read in FITS image
        print 'Reading in master image.'
        self.frame = fits.open(self.master_image, ignore_missing_end = True)[0].data

    # -------------------------------------------------------------------------

    def save_image():
        '''
        Saves the 'master image'.
        '''

        newfile = self.master_image.replace(
            '.fits', '_{}.fits'.format(self.targname))
        fits.writeto(newfile, self.cleaned_frame, header=None, clobber=True)

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def col_image_main(self):
        '''
        The main controller.
        '''

        self.query_qldb()
        self.extract_header_data()
        self.read_image()
        self.remove_columns()
        self.save_image()

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def parse_args():
    '''
    Parse command line arguments. Returns args object.
    '''

    # Create help strings
    targname_help = 'The TARGNAME to use in the Quicklook database query'
    exptime_help = 'The EXPTIME to use in the Quicklook database query'
    master_image_help = 'The relative path of the master image file'

    # Add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--targname', type=str, help=targname_help,
        action='store', required=True)
    parser.add_argument('-e', '--exptime', type=str, help=exptime_help,
        action='store', required=True)
    parser.add_argument('-i', '--master_image', type=str, 
        help=master_image_help, action='store', required=True)

    # Parse args
    args = parser.parse_args()

    return args

# -----------------------------------------------------------------------------

def test_args(args):
    '''
    Ensures valid command line arguments.
    '''

    # Ensure master image exists
    assert os.path.exists(args.master_image) is True, \
        '{} does not exist.'.format(args.master_image)

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    args = parse_args()
    test_args(args)

    col_image = colImage(args.targname, args.exptime, args.master_image)
    col_image.col_image_main()