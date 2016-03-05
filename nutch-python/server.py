import nutch
import argparse
import sys

class NutchClient(object):
    def __init__(self, args):
        self.server = args['server']
        self.conf = args['conf_id']
        self.facade = nutch.Nutch(self.conf, self.server)
        
    # Crawls a specified seed list for n rounds. 
    def doCrawl(self, seed_urls, n):
        cc = self.facade.Crawl(seed=seed_urls, rounds=n)
        
        rounds = cc.waitAll()
        print("Finished: %d rounds" % len(rounds))
        
    
def main(args):
    crawler = NutchClient(args)
    if args['cmd'] == "crawl":
        seed_file = args['seed']
        with open(seed_file) as urls:
            crawler.doCrawl(urls.readlines(), args['num_rounds'])
    else:
        print("Invalid Command : %s" % args['cmd'])
        exit(1)
               
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Nutch REST API Client")
    parser.add_argument("-s", "--server", help="Nutch Server", default="http://localhost:8081")

    subparsers = parser.add_subparsers(help ="sub-commands", dest="cmd")

    crawl_parser = subparsers.add_parser("crawl", help="Runs Crawl Command")    
    crawl_parser.add_argument("-ci", "--conf-id", help="Configuration File", default="default")
    crawl_parser.add_argument("-n", "--num-rounds", required=True, type=int, help="Number of Rounds")
    crawl_parser.add_argument("-url", "--seed", required=True, help="Path to Seed Files")

    args=vars(parser.parse_args(sys.argv[1:]))
    main(args)
