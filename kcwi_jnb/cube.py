import numpy as np
from kcwi_jnb import utils as ku
from astropy.wcs import WCS

class DataCube(object):
    def __init__(self,inp=None,data=None,wavelength=None,include_wcs=True):
        if inp is None:
            dat = data
            filename = ''
            hdr = None
        elif isinstance(inp,str):
            dat,wcs = ku.load_file(inp)
            filename = inp
            hdr = wcs.to_header()
            #self.wcs = wcs
        else:
            dat = inp[0].data
            hdr = inp[0].header
            wcs = WCS(hdr)
            filename = ''

        self.data = dat
        self.header = hdr
        if include_wcs is False:
            self.wcs = None
            self.wavelength = wavelength
        elif include_wcs is True:
            self.wcs = wcs
            self.wavelength = ku.get_wave_arr(dat,self.wcs,extract_wcs=False)
        else:
            self.wcs = include_wcs
            if wavelength is None:
                self.wavelength = ku.get_wave_arr(dat, self.wcs, extract_wcs=False)
            else:
                self.wavelength=wavelength

        self.filename = filename

    def write(self,filename):
        newhdu = self.wcs.to_fits()
        newhdu[0].data = self.data
        newhdu.writeto(filename,overwrite=True)

    def copy(self):
        return