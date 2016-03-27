#!/usr/bin/env python2.7

import nutch
from nutch.nutch import Server
import argparse
import urllib
import sys
import json

DefaultServerEndpoint = 'http://localhost:8081'

TextSendHeader = {'Content-Type': 'text/plain'}
TextAcceptHeader = {'Accept': 'text/plain'}

JsonSendHeader = {'Content-Type': 'application/json'}
JsonAcceptHeader = {'Accept': 'application/json'}

nutch_server = Server(DefaultServerEndpoint, False)

nutch.Verbose = False

# Gets all image links
def getImageURLS(path):
    values = { "path" : path }
    
    key = 'Content-Type=image'
    i = 0
    count = 0
    while True:
        data = nutch_server.call('post', '/reader/sequence/read?start=%s&end=%s' 
                                 % (i, i + 1000), data=values, headers=JsonSendHeader)
        if not data:
            break
        for site in data:
            for meta in site:
                found = meta.find(key)
                if found != -1:
                    count += 1
                    yield site
        i = i + 1000
        
    print "Total Image URLS: %d" %(count)

# Downloads the images
def downloadImages(path, n):
    values = { "path" : path }
    
    extensions = ['.jpeg', '.jpg', '.gif', '.png', '.bmp', '.tif', '.tiff', '.ico']
    counter = 0
    for site in getImageURLS(path):
        for ext in extensions:
            if ext in site[0]:
                try:
                    urllib.urlretrieve(str(site[0]), 'image' + str(counter) + ext)
                    counter += 1
                    break
                except:
                    print 'Unable to Download Image: %s' %(str(site[0]))
        if counter >= n:
            break
        
def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description="Nutch Get Images")
    
    subparsers = parser.add_subparsers(help="sub-commands", dest="cmd")
    url_parser = subparsers.add_parser("url", help="get urls of images")
    url_parser.add_argument("-db", "--db-path", help="path to crawldb sequence files", required=True)
    url_parser.add_argument("-r", "--report", help="path to report",required=True)
    
    download_parser = subparsers.add_parser("get", help="downalods images")
    download_parser.add_argument("-db", "--db-path", help="path to crawldb sequence files", required=True)
    download_parser.add_argument("-n", "--num", help="number of images to download", default=20, type=int)
    
    args=vars(parser.parse_args(argv))
    
    if args['cmd'] == 'url':
        with open(args['report'], 'w') as images:
            for site in getImageURLS(args['db_path']):
                for meta in site:
                    images.write("%s\n" %(meta))
    elif args['cmd'] == 'get':
        downloadImages(args['db_path'], args['num'])
    else:
        print "Invalid Command: %s" % cmd


if __name__ == '__main__':
    main(sys.argv[1:])
