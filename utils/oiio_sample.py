import OpenImageIO as oiio 
import numpy as np
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo


def resize_image(src_image_path, dst_image_path, ratio=0.5):
    dst_image_dir = os.path.dirname(dst_image_path)
    if not os.path.isdir(dst_image_dir):
        os.makedirs(dst_image_dir)
    input_image = oiio.ImageInput.open(src_image_path)
    if not input_image:
        print ('Could not open %s "' % input_image)
        print ("\tError: ", oiio.geterror())
        return
    image_spec = input_image.spec()
    bit = image_spec.format
    channel_num = image_spec.nchannels
    buf_src = oiio.ImageBuf(src_image_path)
    dst = oiio.ImageBuf(oiio.ImageSpec(int(image_spec.width*ratio), int(image_spec.height*ratio), channel_num, bit))
    oiio.ImageBufAlgo.resize(dst, buf_src)
    dst.write(dst_image_path)
    dst.clear()
    buf_src.clear()
    input_image.close()

if __name__ == '__main__':
    input_filename = "test.jpg"
    output_filename = "split_r.jpg"


    # read file
    input_data = oiio.ImageInput.open(input_filename)
    spec = input_data.spec()
    pixels = input_data.read_image ()
    input_data.close()

    out_pixels = np.zeros(pixels.shape)
    out_pixels[:,:,0] = pixels[:,:,0]

    # write file
    output = ImageOutput.create (output_filename)
    output.open (output_filename, spec)
    output.write_image (out_pixels)
    output.close ()
