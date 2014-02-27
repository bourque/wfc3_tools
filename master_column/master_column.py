#! /usr/bin/env python

'''
ABOUT:
This program serves as a wrapper to creates an image of all WFC3 on-orbit 
columns for given TARGNAME and EXPTIME using Jay Anderson's master fits images,
create a file containing metadata that describes the new "master column" image.
'''

import argparse
import os

import make_image
import write_metadata

# -----------------------------------------------------------------------------

def parse_args():
    '''
    Parse command line arguments. Returns args object.
    '''

    # Create help strings
    targname_help = 'The TARGNAME to use in the Quicklook database query'
    exptime_help = 'The EXPTIME to use in the Quicklook database query'
    postflash_help = 'The switch to accept or reject images with ' + \
                     'postflash.  Can be "on" or "off"'
    master_image_help = 'The relative path of the master image file'
    metadata_switch_help = 'If "on", an output file containing "master ' + \
                           'column" metadata will be written to <targname>' + \
                           '_metadata.dat.  if "off", no file will be written.'

    # Add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--targname', type=str, help=targname_help,
        action='store', required=True)
    parser.add_argument('-e', '--exptime', type=str, help=exptime_help,
        action='store', required=True)
    parser.add_argument('-p', '--postflash', type=str, help=postflash_help,
        action='store', required=True)
    parser.add_argument('-i', '--master_image', type=str, 
        help=master_image_help, action='store', required=True)
    parser.add_argument('-m', '--metadata_switch', type=str,
        help=metadata_switch_help, action='store', required=False, 
        default='off')

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

    # Ensure postflash and metadata_switch is either "on" or "off"
    assert args.postflash.lower() in ['on', 'off'], \
        'Argument must be "on" or "off".'
    assert args.metadata_switch.lower() in ['on', 'off'], \
        'Argument must be "on" or "off".'

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    args = parse_args()
    test_args(args)

    make_image = make_image.MakeImage(args.targname, args.exptime,
        args.postflash, args.master_image, args.metadata_switch)
    
    make_image.query_for_rootnames()
    make_image.extract_header_data()
    make_image.read_image()
    make_image.remove_bad_columns()
    make_image.save_image(make_image.cleaned_frame)

    if make_image.metadata_switch.lower() == 'on':
        write_metadata.write_metadata(make_image.targname, 
            make_image.header_data, make_image.qldb_rootnames)