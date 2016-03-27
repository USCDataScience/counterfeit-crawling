import sys
import os
from PIL import Image

# Takes image and returns a list of grayscale values for pixels
def getContent(image_path):
    image = Image.open(image_path).convert('RGB')
    size = (50, 50)
    image.thumbnail(size, Image.ANTIALIAS)
    pixels = list(image.getdata())
    grayscale = [ int(0.3 * pixel[0] + 0.6 * pixel[1] + 0.11 * pixel[2]) for pixel in pixels ]
    return grayscale


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "Usage: %s <path to image> <path to generated output>" % (sys.argv[0])
        sys.exit(-1)

    root_path = sys.argv[1]
    extensions = ['.jpeg', '.jpg', '.gif', '.png', '.bmp', '.tif',
                  '.tiff', '.ico']

    with open(sys.argv[2], 'w') as output:
        for (root, dirs, files,) in os.walk(root_path):
            for file in files:
                for ext in extensions:
                    if ext in file:
                        full_path = root + file
                        content = str(getContent(full_path))
                        output.write('%s\n%s\n\n' % (full_path, content))



