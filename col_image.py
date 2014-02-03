#! /usr/bin/env python

'''
ABOUT:
This program creates an image of all WFC3 on-orbit columns for given TARGNAME,
EXPTIME, and PROPOSID using Jay Anderson's master fits images. It also creates 
an output text file containing the relation between (new) column, rootname, 
and time of observation.
'''

import argparse
from astropy.io import ascii
from astropy.io import fits
import numpy as np
import os
import sqlite3

WORK_DIR = '/grp/hst/wfc3h/bourque/postflash_dark_test/good_pixel_test/'

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

        header_file = os.path.join(WORK_DIR, 'raw2raz_AMPC.hdr')
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
        conn = sqlite3.connect('/Users/bourque/Desktop/ql.db')
        conn.text_factory = str
        db_cursor = conn.cursor()

        # Build query
        command = 'SELECT filename ' + \
                  'FROM UVIS_FLT_0 ' + \
                  'WHERE TARGNAME = "{}" '.format(self.targname) + \
                  'AND EXPTIME = "{}"'.format(self.exptime)

        # Execute query
        db_cursor.execute(command)

        # Parse results
        results = db_cursor.fetchall()
        assert len(results) > 0, 'Query did not yield any resuts.'
        self.qldb_rootnames = [result[0].split('_')[0] for result in results]

        # Close database connections
        conn.close()

 # -------------------------------------------------------------------------

    def query_for_times(self, rootname_list):
        '''
        Queries the Quicklook Database and returns a list of DATE-OBSs and
        TIME-OBS for a list of rootnames.
        '''

        print 'Gathering time information.'

        # Open database connection
        conn = sqlite3.connect('/Users/bourque/Desktop/ql.db')
        conn.text_factory = str
        db_cursor = conn.cursor()

        date_obs_list, time_obs_list = [], []

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
            date_obs_list.extend([result[0] for result in results])
            time_obs_list.extend([result[1] for result in results])

        # Close database connection
        conn.close()

        return date_obs_list, time_obs_list

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
            self.header_data['col'][i] 
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
        self.frame = fits.open(self.master_image, ignore_missing_end = True)[0].data

    # -------------------------------------------------------------------------

    def save_image(self):
        '''
        Saves the 'master image'.
        '''

        newfile = os.path.join(WORK_DIR, self.master_image.replace(
            '.fits', '_{}.fits'.format(self.targname)))
        fits.writeto(newfile, self.cleaned_frame, header=None, clobber=True)
        print 'Saved image to {}'.format(newfile)

    # -------------------------------------------------------------------------

    def write_output(self):
        '''
        Writes an output file containing the relationships between the columns,
        rootnames, and times of observation.
        '''

        # Build dictionary containing data to send to output
        out_dict = {}
        out_dict['columns'] = [self.header_data['col'][i] for i in 
            range(len(self.header_data)) if self.header_data['rootname'][i] 
            in self.qldb_rootnames]
        out_dict['rootnames'] = [self.header_data['rootname'][i] for i in 
            range(len(self.header_data)) if self.header_data['rootname'][i] 
            in self.qldb_rootnames]

        # Query database for DATE-OBS and TIME-OBS for each rootname
        out_dict['date_obs'], out_dict['time_obs'] = \
            self.query_for_times(out_dict['rootnames'])

        # Write results to text file
        outfile = os.path.join(WORK_DIR, 
            self.master_image.replace('.fits', '.dat'))
        ascii.write([out_dict['columns'], out_dict['rootnames'], 
                     out_dict['date_obs'], out_dict['time_obs']], 
                     outfile, 
                     names=['column', 'rootname', 'DATE-OBS', 'TIME-OBS'])

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def col_image_main(self):
        '''
        The main controller.
        '''

        self.query_for_rootnames()
        self.extract_header_data()
        self.read_image()
        self.remove_columns()
        self.save_image()
        self.write_output()

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