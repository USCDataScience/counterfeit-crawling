#!/usr/bin/env python2.7

from nutchpy import sequence_reader
import argparse
import sys
import json

# Dumps all the contents of the crawldb
def getDump(path):
    i = 0
    while True:
        # Reads 1000 at a time to prevent overflow
        data = sequence_reader.slice(i, i + 1000, path)
        if not data:
            break
        for url, meta in data:
            yield url, meta
        i = i + 1000

# Gets a map of mimes and frequency
def getMimes(path):
    mimes = {}
    key = 'Content-Type'
    data = sequence_reader.read_iterator(path)
    
    found = False # Whether metadata for mime type was found
    for url, meta in data:
        for k in meta.keys():
            if k.startswith(key):
                mime = k.split('=')[1]
                mime = mime.strip()
                if mime:
                    mime = mime.strip()
                    mimes[mime] = mimes.get(mime, 0) + 1
                found = True
                break
        if not found:
            mimes["unknown"] = mimes.get("unknown", 0) + 1
    
    print "Total MIME Types: %d" %(len(mimes) - 1)
    return mimes

# Gets a generator for the failed urls    
def getFailed(path):
    failure = {'3 (db_gone)'}
    failed = 0
    data = sequence_reader.read_iterator(path)
    for url, meta in data:
        if 'Status' in meta:
            status = meta.get('Status').strip()
            if status in failure:
                failed += 1
                yield url, meta
        else:
            print "There is no status for %s" %(url)

    print "Failed URLs: %d" %(failed)
    

# Generates crawl statistics
def generate_report(args):
    cmd = args.get('cmd')
    
    if cmd == 'dump':
        with open(args['report'], 'w') as dump:
            for url, meta in getDump(args['crawldb']):
                dump.write("%s\n%s\n" %(url, meta))
    elif cmd == 'failed':
        with open(args['report'], 'w') as failed:
            for url, meta in getFailed(args['crawldb']):
                meta_parsed = json.dumps(meta, indent=4, separators=(',', ': '))
                failed.write("%s\n%s\n" %(url, meta_parsed))
    elif cmd == 'mimes':
        with open(args['report'], 'w') as mimes:
            for mime, count in getMimes(args['crawldb']).iteritems():
                mimes.write("%s, %d\n" %(mime, count))
    else:
        print "Invalid Command : %s" % cmd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Nutch Crawl Statistics")
    
    subparsers = parser.add_subparsers(help ="sub-commands", dest="cmd")
    dump_parser = subparsers.add_parser("dump", help="dumps crawled urls and metadata")
    dump_parser.add_argument("-db", "--crawldb", help="path to crawldb", required=True)
    dump_parser.add_argument("-r", "--report", help="path to report", required=True)
    
    
    failed_parser = subparsers.add_parser("failed", help="dumps failed crawls")
    failed_parser.add_argument("-db", "--crawldb", help="path to crawldb", required=True)
    failed_parser.add_argument("-r", "--report", help="path to report", required=True)

    mime_parser = subparsers.add_parser("mimes", help="scans for different mimes")
    mime_parser.add_argument("-db", "--crawldb", help="path to crawldb", required=True)
    mime_parser.add_argument("-r", "--report", help="path to report", required=True)

    args = vars(parser.parse_args(sys.argv[1:]))
    generate_report(args)
    
    
