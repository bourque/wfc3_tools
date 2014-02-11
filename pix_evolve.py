#! /usr/bin/env python

'''
ABOUT:
This program plots pixel values over time for a given "master image"
'''

import argparse
from astropy.io import ascii
from astropy.io import fits
import datetime
import os
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------

class pixEvolve():
    '''
    Parent class.
    '''

    # -------------------------------------------------------------------------

    def __init__(self, master_image):
        '''
        Assigns argument variables to class instances.
        '''

        self.master_image = master_image

    # -------------------------------------------------------------------------

    def extract_metadata(self):
        '''
        Extracts the metadata associated with the master image from the
        metadata file.
        '''

        metadata_file = 'DARK_metadata.dat'
        print 'Reading data from {}.'.format(metadata_file)
        self.metadata = ascii.read(metadata_file, data_start=1, 
            names=['orig_columns', 'new_columns', 'rootnames', 'date_obs', 
                   'time_obs'])

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
    # -------------------------------------------------------------------------

    def pix_evolve_main(self):
        '''
        The main controller.
        '''

        # Read in master image file
        self.read_image()

        # Read in meta data
        self.extract_metadata()

        # Combine time objects
        col_times = []
        for date_obs, time_obs in zip(self.metadata['date_obs'], self.metadata['time_obs']):
            date = datetime.datetime.strptime(date_obs, '%Y-%m-%d')
            time = datetime.datetime.strptime(time_obs, '%H:%M:%S')
            col_times.append(datetime.datetime.combine(date.date(), time.time()))

        # Create plot
        plt.figure()
        plt.minorticks_on()
        plt.grid()
        plt.xlabel('Time')
        plt.ylabel('Pixel value')
        plt.ylim((-10, 50))

        # Rotate x-axis labels
        plt.setp(plt.xticks()[1], rotation=30)
        plt.gcf().subplots_adjust(bottom=0.15)

        plt.scatter(col_times, self.frame[700,:], s=20, c='k', marker= '+')

        filename = 'test.png'
        plt.savefig(filename)
        print 'Saved figure to {}'.format(filename)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def parse_args():
    '''
    Parse command line arguments. Returns args object.
    '''

    # Create help strings
    master_image_help = 'The relative path of the master image file'

    # Add arguments
    parser = argparse.ArgumentParser()
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

    # Ensure data file exists
    data_file = 'DARK_metadata.dat'
    assert os.path.exists(data_file) is True, \
        '{} does not exist.'.format(data_file)

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    args = parse_args()
    test_args(args)

    pix_evolve = pixEvolve(args.master_image)
    pix_evolve.pix_evolve_main()