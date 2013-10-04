import sys
import pyfits
import wfc3tools
from wfc3tools import calwf3

AUTHOR:
Mike Dulude
STScI
dulude@stsci.edu

'''

This code resets the TDFTRANS header keyword to zero and reprocesses with the lastest 
version of CALWF3. 
if not already zero, the value of sci ext header keyword TDFTRANS is reset to zero.
If not already set to OMIT, the PHOTCORR, and DRIZCORR header values are set to OMIT.
INPUTS(1)
name of ascii text file containing list of raw WFC3/IR observations to be reprocessed, one per line.
'''
#---------------------------------------------------------------------------------

def do_tdf_fix(imagename):
	#summery: uses pyfits.setval to change tdftrans value to zero in all sci extensions
	nsamp = pyfits.getval(imagename, "NSAMP", 0)
	for samp_ctr in range(1,nsamp+1):
		tdfval = pyfits.getval(imagename, "TDFTRANS", ('sci',samp_ctr))
		if tdfval != 0:
			pyfits.setval(imagename, "TDFTRANS", value=0, ext=('sci',samp_ctr))
	return imagename
#---------------------------------------------------------------------------------



filename=sys.argv[1]

inf = open(filename)
fitsfilelist = inf.readlines()
inf.close()

for fits_filename in fitsfilelist:
	fits_filename = fits_filename.strip()
	blarg = do_tdf_fix(fits_filename)
	#pyfits.setval(fits_filename, "PHOTCORR", value='OMIT', ext=0)
	#pyfits.setval(fits_filename, "DRIZCORR", value='OMIT', ext=0)
	calwf3.calwf3(fits_filename)
