import OpenImageIO as oiio 
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo


if __name__ == "__main__":
    buf_jpg = ImageBuf("test.jpg")
    buf_exr = ImageBuf("test2.exr")
    buf_tga = ImageBuf("test3.tga")
    buf_png = ImageBuf("test4.png")
    input_data = oiio.ImageInput.open("test3.tga")
    spec = input_data.spec()
    print(spec.format)

    # print(buf_jpg.get_pixels(oiio.UINT8))
    # print(buf_exr.get_pixels(oiio.UINT8))

    # print(dir(buf_jpg.spec()))
    print(buf_jpg.spec().getattribute('oiio:ColorSpace'))
    print(buf_exr.spec().getattribute('oiio:ColorSpace'))
    print(buf_tga.spec().getattribute('oiio:ColorSpace'))
    print(buf_png.spec().getattribute('oiio:ColorSpace'))
