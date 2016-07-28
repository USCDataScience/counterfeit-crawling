#!/usr/bin/env python2.7

import argparse
import sys

# Get failed urls and reason from hadoop.log
def getFailed(path):
    for line in open(path):
        if 'failed with' in line:
            yield line[line.find('INFO') + 4:].strip()

def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description="Looks through Hadoop Log for Failures")
    parser.add_argument("-f", "--log", help="path to hadoop.log", required=True)
    parser.add_argument("-r", "--report", help="path to report", required=True)
    
    args = vars(parser.parse_args(argv))
    
    with open(args['report'], 'w') as failed:
        for item in getFailed(args['log']):
            failed.write("%s\n" %(item))
            
    
if __name__ == '__main__':
    main(sys.argv[1:])
