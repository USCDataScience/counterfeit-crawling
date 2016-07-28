#!/usr/bin/env python2.7

import requests
import argparse
import sys
import json
import os
from urlparse import urlparse

DefaultServerEndpoint = 'http://localhost:8081'

TextSendHeader = {'Content-Type': 'text/plain'}
TextAcceptHeader = {'Accept': 'text/plain'}

JsonSendHeader = {'Content-Type': 'application/json'}
JsonAcceptHeader = {'Accept': 'application/json'}


def getData(root_path):
    import glob
    
    regex_path = root_path + '/crawl-*/segments/*/parse_data/part-*/data'
    return glob.glob(regex_path)


def generate_report(args):
    images = {}
    total = {}
    
    key = 'Content-Type'
    for path in getData(args['path']):
        path = os.path.abspath(path)
        
        print "Handling path ", path
        
        values = { "path" : path }
        extensions = ['jpeg', 'jpg', 'gif', 'png', 'bmp', 'tif', 'tiff', 'ico']
        
        i = 0
        while True:
            try:
                response = requests.post('http://localhost:8081/reader/sequence/read?start=%s&end=%s' 
                                     % (i, i + 1000), data=json.dumps(values), headers=JsonSendHeader)
            except Exception as e:
                print e
                break
            
            if (response.status_code != requests.codes.ok):
                print "Path %s failed: " % path, response.text
                break
                
            data = response.json()
            if not data:
                break
            
            for element in data:
                site = element[0].lower()
                print site

                url = urlparse(site)
                domain = url.netloc
                total[domain] = total.get(domain, 0) + 1
                
                site_list = site.encode('utf-8').split('.')
                if site_list[-1].lower() in extensions:
                    images[domain] = images.get(domain, 0) + 1
                            
    with open(args['report'] + '/images.txt', 'w+') as o:
        for host, count in images.iteritems():
            o.write('%s, %d\n' %(host.decode('utf-8'), count))
                 
    with open(args['report'] + '/total.txt', 'w+') as o:
        for host, count in total.iteritems():
            o.write('%s, %d\n' %(host.decode('utf-8'), count))
         
             
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Nutch Crawl Statistics")
    
    parser.add_argument("-p", "--path", help="path to crawldb", required=True)
    parser.add_argument("-r", "--report", help="path to report", required=True)

    args = vars(parser.parse_args(sys.argv[1:]))
    generate_report(args)
    
