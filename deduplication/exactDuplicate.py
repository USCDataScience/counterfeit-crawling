#!/usr/bin/env python2.7  

import sys
from hashlib import md5
import re

# Hashes the byte representation of the image using md5
def hash_image(image):
    # Check if input is URL or path to file
    match = re.match(r'(ftp|https|http)://.*', image, re.M|re.I)
    if match is None: # Path to file, not URL
        image_bytes = open(image).read()
        image_hash = md5(image_bytes).hexdigest()
        return image_hash
    else:
        img = urllib.urlopen(image)

        image_bytes = img.read()
        image_hash = md5(image_bytes).hexdigest()
        return image_hash


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'Usage: %s <path to dump file> <path to created ouput file>' % (sys.argv[0])
        sys.exit(-1)

    from common import readDump
    
    file_path = sys.argv[1]
    images = readDump(file_path)
    
    images_dedup = {}
    for image in images.keys():
        image_hash = hash_image(image)
        
        # Create entry if hash doesn't exist
        if images_dedup.get(image_hash) is None:
            images_dedup[image_hash] = []

        images_dedup[image_hash].append(image)
    
    # Writes unique entries to separate file. Chooses arbitrarily among the 
    # duplicates
    with open(sys.argv[2], 'w') as output:
        for hash in images_dedup.keys():
            output.write('%s\n' %(images_dedup[hash][0]))
    
    print "Total Images: ", len(images.keys())
    print "Unique Images: ", len(images_dedup.keys())
