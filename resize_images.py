# image libraries
import PIL
from PIL import Image

# os libraries
import glob, os


# TODO take this value as a parameter
SQUARE_SIZE = 96
# TODO take this value as a parameter
DEFAULT_DIR = '../images'

def resize_images():
    # script setup
    directory = DEFAULT_DIR
    file_filter = '*.png'
    resize_to = SQUARE_SIZE

    # change the current directory to the one that contains the images
    os.chdir(directory)
    # list all the files with the given filter
    files = glob.glob(file_filter)
    # debugging
    print 'moving to directory', directory
    print 'applying filter', file_filter
    print 'files found', len(files)

    # iterate the files
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        print 'resizing image', file
        _resize_image(file_name, file_extension, resize_to)

def _resize_image(image_name, image_extension, basewidth):
    img = Image.open(image_name + image_extension)
    img = img.resize((basewidth, basewidth), PIL.Image.ANTIALIAS)
    img.save(image_name + '_' + str(basewidth) + image_extension)

resize_images()
