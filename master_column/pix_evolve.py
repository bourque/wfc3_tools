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
import numpy as np

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

    def average_month(self, row, col_times):
        '''
        Returns a list of monthly averaged pixel values.
        '''

        num_months = (col_times[-1] - col_times[0]).days / 30
        avg_pix_list, avg_time_list = [], []

        pixels = self.frame[row,:]

        start_dates = [col_times[0]]
        for i in range(num_months):
            start_dates.append(start_dates[-1] + datetime.timedelta(30))

        end_dates = [col_times[0] + datetime.timedelta(30)]
        for i in range(num_months):
            end_dates.append(end_dates[-1] + datetime.timedelta(30))

        for start, end in zip(start_dates, end_dates):
            month_pixels = [pix for pix, time in zip(pixels, col_times) if start <= time < end]
            month_average = np.median(month_pixels)
            avg_pix_list.append(month_average)
            avg_time_list.append(end)

        return avg_pix_list, avg_time_list

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

    def get_good_rows(self):
        '''
        Uses the bad pixel stack image ("badpix.fits") to determine which
        rows have "good pixels" for the given column.  
        '''

        col = int(self.master_image.split('_')[1][2:5]) - 25
        badpix_stack = fits.open('badpix.fits', 
                               ignore_missing_end = True)[0].data
        print col
        badpix_stack_col = badpix_stack[:, col - 1]
        print badpix_stack_col
        row_list = np.where(badpix_stack_col == 0)[0]
        print row_list

        return row_list

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

        # Set plotting parameters
        plt.figure()
        plt.minorticks_on()
        plt.grid()
        plt.xlabel('Time')
        plt.ylabel('30-day Average Pixel value')
        plt.ylim((-2, 50))
        plt.setp(plt.xticks()[1], rotation=30)
        plt.gcf().subplots_adjust(bottom=0.15)

        row_list = self.get_good_rows()
        #row_list = [2]
        for row in row_list:
            avg_pix_list, avg_time_list = self.average_month(row, col_times)
            if avg_pix_list[2] > 400:
                print row, avg_pix_list

            plt.scatter(avg_time_list, avg_pix_list, s=20, c='k', marker= '+')

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