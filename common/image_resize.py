from PIL import Image
from resizeimage import resizeimage
import glob
import os

"""
# Pass inout file path , output file and desired size in pixels
# Please note we need to use PIL version 2.9 - Latest version of PIL does not work and has bug
# below is an example
def resize_file(in_file, size):
    with open(in_file,'r+b') as fd:
        with Image.open(fd) as image:
            cover = resizeimage.resize_cover(image, size)
            #cover.save(out_file,image.format)
            cover.save(in_file, image.format)
            image.close
            cover.close

for filename in glob.glob(r'C:\Users\Desktop\Desktop\flask\pikuhomes\app\static\img\pg1\*.jpg'):
    print "Resizing " + filename
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    resize_file(filename, basename, (420, 218))
"""
#http://stackoverflow.com/questions/9103257/resize-image-maintaining-aspect-ratio-and-making-portrait-and-landscape-images-e
from PIL import Image, ImageChops, ImageOps

def resize_file(in_file, size=(640, 427)):

    image = Image.open(in_file)
    image.thumbnail(size, Image.ANTIALIAS)
    image_size = image.size


    thumb = image.crop( (0, 0, size[0], size[1]) )

    offset_x = max( (size[0] - image_size[0]) / 2, 0 )
    offset_y = max( (size[1] - image_size[1]) / 2, 0 )
    thumb = ImageChops.offset(thumb, offset_x, offset_y)

    thumb.save(in_file)