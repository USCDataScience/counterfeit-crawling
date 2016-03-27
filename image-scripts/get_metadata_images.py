#!/usr/bin/env python2.7

import nutch
from nutch.nutch import Server
import argparse
import sys
import json
import os
import urllib

DefaultServerEndpoint = 'http://localhost:8081'

TextSendHeader = {'Content-Type': 'text/plain'}
TextAcceptHeader = {'Accept': 'text/plain'}

JsonSendHeader = {'Content-Type': 'application/json'}
JsonAcceptHeader = {'Accept': 'application/json'}

nutch_server = Server(DefaultServerEndpoint, False)

nutch.Verbose = False

def getSegments(path):
    import glob

    regex_path = path + '/*/content/part-*/data'
    return glob.glob(regex_path)
    

# Returns image url, and concatenated string of metadata values   
def getImageMeta(path, n):
    from normalize_images import getContent

    values = {"path" : path }

    extensions = ['jpeg', 'jpg', 'gif', 'png', 'bmp', 'tif', 'tiff', 'ico']

    i = 0
    while True:
        # Reads 1000 at a time to prevent overflow
        data = nutch_server.call('post', '/reader/sequence/read?start=%s&end=%s' 
                                 % (i, i + 1000), data=values, headers=JsonSendHeader)
        if not data:
            break
        if n == 0:
            break
        for element in data:
            site = element[0].lower()
            site_list = site.encode('utf-8').split('.')
            
            if site_list[-1].lower() in extensions:
                metadata = ''.join(meta + ';' for meta in element[1] if meta.isalnum())
                
                # Download the image into temporary file
                temp_file = 'temp.' + site_list[-1]
                f = open(temp_file, 'wb')
                img = urllib.urlopen(line_url)
                f.write(img.read())
                f.close()
                
                # Read the pixel content of image, and append to metadata 
                full_path = os.getcwd() + temp_file
                image_pixels = getContent(full_path)
                
                metadata = metadata.join(str(i) for i in image_pixels)
                
                # Remove the temporary file
                os.remove(temp_file)

                yield site, metadata.encode('ascii', 'ignore')
                
                n -= 1
                if n == 0:
                    break
                
        i = i + 1000


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description="Nutch Crawl Statistics")

    subparsers= parser.add_subparsers(help="sub-commands", dest="cmd")
    image_parser = subparsers.add_parser("dump", help="dumps crawled image metadata")
    image_parser.add_argument("-db", "--db-path", help="path to segment sequence files", required=True)
    image_parser.add_argument("-r", "--report", help="path to report", required=True)
    image_parser.add_argument("-n", "--num", help="number of images", type=int, default=100)

    args = vars(parser.parse_args(argv))
    
    if args['cmd'] == 'dump':
        with open(args['report'], 'w') as dump:
            for path in getSegments(args['db_path']):
                for url, meta in getImageMeta(path, args['num']):
                    dump.write('%s\n%s\n\n' % (url, meta))
    else:
        print "Invalid Command : %s" % args['cmd']
                     
if __name__ == '__main__':
    main(sys.argv[1:])
