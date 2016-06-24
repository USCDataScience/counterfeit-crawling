#!/usr/bin/env python2.7

import argparse
import sys
import xlwt

# Get failed urls and reason from hadoop.log
def getFailed(path):
    errors = {}
    failed = 0
    for line in open(path):
        line = line.decode("utf-8")
        if 'failed with' in line:
            failed += 1
            try:
                start = line.rindex('with: ')
                error = line[start:]
            except ValueError:
                continue
            errors[error] = errors.get(error, 0) + 1
    print "Total Errors: %d" %(failed)        
    return errors

def getURLS(path):
    from urlparse import urlparse

    urls = {}
    for line in open(path):
        line = line.decode("utf-8")
        if 'failed with' in line:
            try:
                start = line.index('of ')
                end = line.index('failed')
                link = line[start + 3:end - 6]
                url = urlparse(link)
            except ValueError:
                continue
            urls[url.netloc] = urls.get(url.netloc, 0) + 1
    print "Total URL Hosts Failed: %d" %(len(urls))        
    return urls

def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description="Looks through Hadoop Log for Failures")
    parser.add_argument("-f", "--log", help="path to hadoop.log", required=True)
    parser.add_argument("-r", "--report", help="path to report", required=True)
    
    args = vars(parser.parse_args(argv))
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Errors")
    
    ws.write(0, 0, "Error")
    ws.write(0, 1, "# Occurences")
    
    i = 1
    for error, num in getFailed(args['log']).iteritems():
        ws.write(i, 0, error)
        ws.write(i, 1, num)
        i += 1

    ws_2 = wb.add_sheet("Failed URLs")
    ws_2.write(0, 0, "Failed URL Hosts")
    ws_2.write(0, 1, "# Occurences")
    
    i = 1
    for url, num in getURLS(args['log']).iteritems():
        ws_2.write(i, 0, url)
        ws_2.write(i, 1, num)
        i += 1

    wb.save(args['report'])
    
if __name__ == '__main__':
    main(sys.argv[1:])
