#!/usr/bin/env python2.7  

import sys
import os

import tika
from tika import parser

def parseImage(image_path):
    import re
    from normalize_images import getContent

    parsed = parser.from_file(image_path)
    # print parsed["metadata"]
    
    metadata = parsed.get("metadata", {})
    
    image_data = ''
    features = ['Content-Type', 'tiff:ImageWidth', 'tiff:ImageLength', 'File Size', 'Pixels']
    
    image_pixels = getContent(image_path)
    metadata['Pixels'] = ''.join([str(i) for i in image_pixels])
    
    image_data = image_data.join(feature + ':' + metadata.get(feature, "None") + ';' 
                                 for feature in features)
        
    return re.sub(r'\s+', '', image_data)
        
if __name__ == '__main__':
    if (len(sys.argv)) != 3:
        print 'Usage: %s <path to images directory> <path to created dump file>' % (sys.argv[0])
        sys.exit(-1)

    root_path = sys.argv[1]
    if root_path[-1] != '/':
        root_path += '/'

    extensions = ['.jpeg', '.jpg', '.gif', '.png', '.bmp', '.tif', '.tiff', '.ico']    
    with open(sys.argv[2], 'w') as output:
        for (root, dirs, files) in os.walk(root_path):
            for file in files:
                for ext in extensions:
                    if ext in file:
                        full_path = root + file
                        print full_path
                        metadata = parseImage(full_path)
                        output.write('%s\n%s\n\n' %(full_path, metadata))
                        
