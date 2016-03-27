#!/usr/bin/env python2.7   

import sys

def readDump(path):
    image_extensions = ['jpeg', 'jpg', 'gif', 'png', 'bmp', 'tif',
                        'tiff', 'ico']
    
    output = {}
    with open(path, 'r') as f:
        while True:
            line = f.readline();
            if not line: 
                break
            if line.strip():
                ext = line.split('.')[-1].strip().lower()
                if ext in image_extensions:
                    line2 = f.readline()
                    output[line.strip()] = line2.strip()
    return output

if __name__ == '__main__':
    path = sys.argv[1]
    print str(readDump(path))
