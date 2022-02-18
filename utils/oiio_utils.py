'''
oiio_utils.py

This is to get basic functions using open image io.
'''

import OpenImageIO as oiio 
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo

def open_image_file(filename):
    '''
    image file -> ndarray, oiio data spec
    '''
    input_data = oiio.ImageInput.open(filename)
    if not input_data:
        print ('Could not open %s "' % input_image)
        print ("\tError: ", oiio.geterror())
        return
    spec = input_data.spec()
    pixels = input_data.read_image()
    input_data.close()
    return pixels, spec


def normalize_from_bit_to_int(pixels):
    pixels = cv2.normalize(pixels, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
    pixels = pixels.astype(np.uint8)
    return pixels
    

def get_channel(pixels):
    pass