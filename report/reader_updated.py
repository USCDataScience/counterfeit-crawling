#!/usr/bin/env python2.7

import nutch
from nutch.nutch import Server
import argparse
import sys
import json

DefaultServerEndpoint = 'http://localhost:8081'

TextSendHeader = {'Content-Type': 'text/plain'}
TextAcceptHeader = {'Accept': 'text/plain'}

JsonSendHeader = {'Content-Type': 'application/json'}
JsonAcceptHeader = {'Accept': 'application/json'}

nutch_server = Server(DefaultServerEndpoint, False)

nutch.Verbose = False

def getSegments(root_path):
    import glob

    regex_path = root_path + '/current/part-*/data'
    return glob.glob(regex_path)


def dict_to_string(dictionary, ident = ''):
    """ Recursively prints nested dictionaries."""

    ret = ""
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            ret += '%s%s:\n' %(ident, key) 
            ret += dict_to_string(value, ident+'    ')
        else:
            ret += ident+'%s = %s\n' %(key, value)
    return ret

# Gets Crawl Summary Stats
def getStats(db, conf):
        values = {"type" : "stats", "confId": conf, 
                  "crawlId": db}
        data = nutch_server.call('post', '/db/crawldb', data=values, 
                                 headers=JsonAcceptHeader)
        data_dump = json.dumps(data)
        return json.loads(data_dump)


# Dumps all the contents of the crawldb
def getDump(path, n):
    values = { 'path' : path }
    i = 0
    while True:
        # Reads 1000 at a time to prevent overflow
        data = nutch_server.call('post', '/reader/sequence/read?start=%s&end=%s' 
                                 % (i, i + 1000), data=values, headers=JsonSendHeader)
        if not data:
            break
        for site in data:
            if n == 0:
                break
            n -= 1
            yield site
        i = i + 1000


# Gets a map of mimes and frequency
def getMimes(root_path):
    mimes = {}
    key = 'Content-Type'
    
    for path in getSegments(root_path):
        values = { "path" : path }

        i = 0
        while True:
            data = nutch_server.call('post', '/reader/sequence/read?start=%s&end=%s' 
                                     % (i, i + 1000), data=values, headers=JsonSendHeader)
            if not data:
                break
            # print data
            for site in data:
                for meta in site:
                    found = meta.find(key)
                    if found != -1:
                        begin = meta.find('=', found) + 1
                        end = meta.find('\n', begin)
                        mime = meta[begin:end].strip()
                        mimes[mime] = mimes.get(mime, 0) + 1
                        break
                    else:
                        mimes['unknown'] = mimes.get('unknown', 0) + 1
            i = i + 1000
                        
    print "Total MIME Types: %d" %(len(mimes) - 1)
    return mimes
        
# Gets number of pages from each host 
def getHosts(root_path):
    from urlparse import urlparse
    hosts = {}
    
    for path in getSegments(root_path):
        values = {"path" : path}
        
        i = 0
        while True:
            data = nutch_server.call('post', '/reader/sequence/read?start=%s&end=%s' 
                                     % (i, i + 1000), data=values, headers=JsonSendHeader)
            if not data:
                break
            # print data
            for site in data:
                for meta in site:
                    url = urlparse(meta)
                    if (url.scheme != ''):
                        hosts[url.netloc] = hosts.get(url.netloc, 0) + 1
                        break
            i = i + 1000
    print "Total Hosts: %d" % (len(hosts))
    return hosts
                
                
# Gets a generator for the failed urls    
def getFailed(path):    
    values = { 'path' : path }
    
    failure = '3 (db_gone)'
    failed = 0
    i = 0
    while True:
        # Reads 1000 at a time to prevent overflow
        data = nutch_server.call('post', '/reader/sequence/read?start=%s&end=%s' 
                                 % (i, i + 1000), data=values, headers=JsonSendHeader)
        if not data:
            break
        for site in data:
            for meta in site:
                found = meta.find(failure)
                if found != -1:
                    failed += 1
                    yield site
        i = i + 1000
    
    print "Failed URLs: %d" %(failed)


# Generates crawl statistics
def generate_report(args):
    cmd = args.get('cmd')
    
    if cmd == 'stats':
        with open(args['report'], 'w') as stats:
            dict = getStats(args['db_name'], args['conf'])
            stats.write(dict_to_string(dict))
    elif cmd == 'dump':
        with open(args['report'], 'w') as dump:
            for path in getSegments(args['db_path']):
                for site in getDump(path, args['num']):
                    for meta in site:
                        dump.write("%s\n" %(meta))
    elif cmd == 'failed':
        with open(args['report'], 'w') as failed:
            for path in getSegments(args['db_path']):
                for site in getFailed(path):
                    for meta in site:
                        failed.write("%s\n" %(meta))
    elif cmd == 'mimes':
        with open(args['report'], 'w') as mimes:
            for mime, count in getMimes(args['db_path']).iteritems():
                mimes.write("%s, %d\n" %(mime, count))
    elif cmd == 'hosts':
        with open(args['report'], 'w') as hosts:
            for host, count in getHosts(args['db_path']).iteritems():
                hosts.write('%s, %d\n' %(host.decode('utf-8'), count))
    else:
        print "Invalid Command : %s" % cmd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Nutch Crawl Statistics")
    
    subparsers = parser.add_subparsers(help ="sub-commands", dest="cmd")
    stats_parser = subparsers.add_parser("stats", help="returns crawl stats")
    stats_parser.add_argument("-db", "--db-name", help="name of folder containing crawldb", required=True)
    stats_parser.add_argument("-cid", "--conf", help="configuration id", default = "default")
    stats_parser.add_argument("-r", "--report", help="path to report", required=True)
    
    dump_parser = subparsers.add_parser("dump", help="dumps crawled urls and metadata")
    dump_parser.add_argument("-p", "--db-path", help="path to crawldb", required=True)
    dump_parser.add_argument("-r", "--report", help="path to report", required=True)
    dump_parser.add_argument("-n", "--num", help="number of urls", default=5000, type=int)

    failed_parser = subparsers.add_parser("failed", help="dumps failed crawls")
    failed_parser.add_argument("-p", "--db-path", help="path to crawldb", required=True)
    failed_parser.add_argument("-r", "--report", help="path to report", required=True)

    mime_parser = subparsers.add_parser("mimes", help="scans for different mimes")
    mime_parser.add_argument("-p", "--db-path", help="path to crawldb", required=True)
    mime_parser.add_argument("-r", "--report", help="path to report", required=True)


    host_parser = subparsers.add_parser("hosts", help="scans for different hosts")
    host_parser.add_argument("-p", "--db-path", help="path to crawldb", required=True)
    host_parser.add_argument("-r", "--report", help="path to report", required=True)

    args = vars(parser.parse_args(sys.argv[1:]))
    generate_report(args)
