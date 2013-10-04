#! /usr/bin/env python
'''
ABOUT:
This program identifies old result*.xml files in the WFC3 file system and 
deletes them.

DEPENDS:
Python 2.7.1

AUTHOR:
Matthew Bourque
Space Telescope Science Institute
bourque@stsci.edu

LAST UPDATED:
10/16/12 (Bourque)
'''

import os
import glob

if __name__ == '__main__':

    root_list = ['/grp/hst/wfc3a/Quicklook/', '/grp/hst/wfc3f/QL_GO/',
                 '/grp/hst/wfc3g/QL_GO/']

    xml_list = []

    for root in root_list:
        for path, subdirs, files in os.walk(root):
            path_elements = path.split('/')
            if 'Persist' not in path_elements:
                for file in files:
                    file_path = os.path.join(path, file)
 
                    if '.xml' in file_path:
                        print file_path

#                    if 'result' in file_path and file_path[-4:] == '.xml':
#                        print file_path
#                        os.remove(file_path)


