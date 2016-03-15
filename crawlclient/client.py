#!/usr/bin/env python2.7

import nutch
from nutch.nutch import Server
import argparse
import sys

TextSendHeader = {'Content-Type': 'text/plain'}
TextAcceptHeader = {'Accept': 'text/plain'}

JsonAcceptHeader = {'Accept': 'application/json'}

class NutchClient(object):
    def __init__(self, args):
        self.server = args['server']
        self.conf = args['conf_id']
        self.facade = nutch.Nutch(confID=self.conf, serverEndpoint=self.server, raiseErrors=False)
        
        # nutch_server = Server(self.server, False)
        # list = nutch_server.call('get', "/config")
        
    # Crawls a specified seed list for n rounds. 
    def doCrawl(self, seed_urls, n):
        cc = self.facade.Crawl(seed=seed_urls, rounds=n)
        
        rounds = cc.waitAll()
        print("Finished: %d rounds" % len(rounds))
        
    # Sets a configuration given a .xml file
    def createConf(self, file, id):
        import xml.etree.ElementTree as ET

        tree = ET.parse(file)
        root = tree.getroot()
        
        configs = {}
        for property in root.findall('property'):
            configs[property.find('./name').text.strip()] = property.find('./value').text.strip()
         
        nutch_server = Server(self.server, False)
        configArgs = {'configId': id, 'params': configs, 'force': True}
        cid = nutch_server.call('post', "/config/create", configArgs, forceText=True, 
                                headers=TextAcceptHeader)
        
        # Returns error for some reason?
        # cid = self.facade.Configs().create(id, configs)
        

def main(args):
    crawler = NutchClient(args)

    if args['cmd'] == "crawl":
        seed_file = args['seed']
        with open(seed_file) as urls:
            crawler.doCrawl(urls.readlines(), args['num_rounds'])
    elif args['cmd'] == "conf":
        crawler.createConf(args['file'], args['id'])
    else:
        print("Invalid Command : %s" % args['cmd'])
        exit(1)

               
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Nutch REST API Client")
    parser.add_argument("-s", "--server", help="Nutch Server", default="http://localhost:8081")
    parser.add_argument("-ci", "--conf-id", help="Configuration Id", default="default")
    
    subparsers = parser.add_subparsers(help ="sub-commands", dest="cmd")

    crawl_parser = subparsers.add_parser("crawl", help="Runs Crawl Command")
    crawl_parser.add_argument("-n", "--num-rounds", required=True, type=int, help="Number of Rounds")
    crawl_parser.add_argument("-url", "--seed", required=True, help="Path to Seed Files")
    
    conf_parser = subparsers.add_parser("conf", help="Adds Configuration")
    conf_parser.add_argument("-id", "--id", required=True, help="New Configuration Id")
    conf_parser.add_argument("-f", "--file", required=True, help="Path to configuration file")
    
    args=vars(parser.parse_args(sys.argv[1:]))
    main(args)
