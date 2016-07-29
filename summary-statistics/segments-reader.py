#!/usr/bin/env python2.7

import sys, getopt
import glob
import string
import operator
import codecs
import robotparser

from urlparse import urlparse

import httplib
import urllib
import re
import sys

import signal

class TimeoutError(Exception):
    pass


def handleTimeout(signum, frame):
    print "Timeout occured"
    
    raise TimeoutError("Timeout. Quitting function...")


def checkUrl(url):
    """
    Check if a URL exists
    """
    import socket
    socket.setdefaulttimeout(5)

    try:
        p = urlparse(url)
        conn = httplib.HTTPConnection(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        return resp.status < 400
    except Exception ,e:
        raise
        return False
    
    
def checkRobots(domain_url):
    parser = robotparser.RobotFileParser()
    
    # HTTP errors and robots.txt bans are grouped together
    try:
        parser.set_url(domain_url + '/robots.txt')        
        parser.read()
        
        if parser.can_fetch('*', domain_url):
            return True
        else:
            return False
    except Exception, e:
        raise
        return False                               
                   

def hasLogin(url):
    """
    Detect if a certain URL has a login form
    """
    try:
        f = urllib.urlopen(url)
        html = f.read()
    except:
        raise
        return False
    
    pattern_password = r'<[a-z]+.*?(type="password"|name="password").*?>'
    pattern_login = r'<a.*?>(((l|L)og|(s|S)ign) (i|I)n)</a>'
    
    search = re.search(pattern_password, html, re.I)
    if search:
       return True
    
    search = re.search(pattern_login, html, re.I)
    if search:
        return True
    
    return False



def getSummaryStats(input_dir, output_dir):
    """
    Gets the following statistics by reading the Nutch segments dump:
    - Total Unique Domains
    - # of Pages per Domain
    - # of Images per Domain
    - Domains with robots.txt that Ban Crawling
    - Domains with Login Forms
    """
    
    files = glob.glob(input_dir + '/*/dump')
    total = {}
    images = {}

    total_num = 0
    images_num = 0
    
    robots_banned = 0
    robots_allowed = 0
    
    login_num = 0
    
    timeout_num = 0
    # Keep track of banned domains
    banned = codecs.open(output_dir + '/banned.txt', 'w', 'utf-8')
    login = codecs.open(output_dir + '/login.txt', 'w', 'utf-8')
    domain_urls = codecs.open(output_dir + '/domains.txt', 'w', 'utf-8')
    all_urls = codecs.open(output_dir + '/all_urls.txt', 'w', 'utf-8')
    timeout = codecs.open(output_dir + '/timeout.txt', 'w', 'utf-8')
    
    # Use extensions to detect image URLs
    extensions = ['jpeg', 'jpg', 'gif', 'png', 'bmp', 'tif', 'tiff', 'ico']
    
    signal.signal(signal.SIGALRM, handleTimeout)
    
    for f in files:
        print "Checking ... ", f
        sys.stdout.flush()
        
        fileRead = open(f, 'r')
        for line in fileRead:
            if line.startswith('URL'):
                url = line[line.find('::') + 2:].strip()
                all_urls.write('%s\n' % url.decode('utf-8'))
                
                url_parsed = urlparse(url)
                
                domain = url_parsed.netloc
                
                # Read the domain for a robots.txt, if it is first time seeing that domain
                if total.get(domain, 0) == 0:
                    domain_url = url_parsed.scheme + '://' + url_parsed.netloc
                    domain_urls.write('%s\n' % domain_url.decode('utf-8'))
                    
                    print "Reading /robots.txt: ", domain_url
                    sys.stdout.flush()
                    
                    signal.alarm(5)
                    
                    try:
                        if checkRobots(domain_url + '/robots.txt'):
                            robots_allowed += 1
                        else:
                            banned.write('%s\n' % domain.decode('utf-8'))
                            robots_banned += 1
                        
                            print "Banned: ", domain
                            sys.stdout.flush()
                    except TimeoutError, e:
                        timeout_num += 1
                        timeout.write('%s\n' % domain_url.decode('utf-8'))

                        print "%s: " % domain_url, e
                        sys.stdout.flush()
                    except:
                        continue
                    
                    signal.alarm(0)
                    
                    print "Scanning for login: ", domain_url
                    sys.stdout.flush()
                   
                    signal.alarm(3)

                    # The login is slowed down by the http requests to get raw html. Use the java
                    # implementation to get straight from Nutch segments dump.
                    """ 
                    try:
                        # Check if the page contains a login form
                        if hasLogin(domain_url):
                            login_num += 1
                            print "Login: ", domain
                            sys.stdout.flush()
                        
                            login.write('%s\n' % domain.decode('utf-8'))
                    except TimeoutError, e:
                        timeout_num += 1
                        timeout.write('%s\n' % domain_url.decode('utf-8'))
                        
                        print "%s: " % domain_url, e
                        sys.stdout.flush()
                    except:
                        continue
                    
                    signal.alarm(0)
                    """
                    
                total_num += 1
                total[domain] = total.get(domain, 0) + 1
                
                site_list = url_parsed.path.split('.')
                if site_list[-1] in extensions:
                    images_num += 1
                    images[domain] = images.get(domain, 0) + 1
        fileRead.close()
    
    print "Total: ", total_num
    print "Images: ", images_num
    print "Total Domains: ", len(total)
    print
    print "Robots Allowed: ", robots_allowed
    print "Robots Banned: ", robots_banned
    sys.stdout.flush()
    
    # Write to output files
    errors = 0
    
    with codecs.open(output_dir + '/total.txt', 'w', 'utf-8') as o:
        sorted_total = sorted(total.items(), key=operator.itemgetter(1), reverse=True)
        for host, count in sorted_total:
            host = host.decode('utf-8')
            try:
                o.write('%s, %d\n' %(host, count))
            except:
                errors += 1

    with codecs.open(output_dir + '/images.txt', 'w', 'utf-8') as o:
        sorted_images = sorted(images.items(), key=operator.itemgetter(1), reverse=True)
        for host, count in sorted_images:
            host = host.decode('utf-8')
            try:
                o.write('%s, %d\n' %(host, count))
            except:
                continue

    print "Error Domains: ", errors
    
    # Close files
    banned.close()
    login.close()
    domain_urls.close()
    all_urls.close()
    timeout.close()


def main(argv=sys.argv):
    usage = "segment-reader.py -i <input_dir> -o <output_dir>"
    input = ""
    output = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:")
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit(2)
        elif opt == '-i':
            input = arg
        elif opt == '-o':
            output = arg

    getSummaryStats(input, output)


if __name__ == '__main__':
    main(sys.argv[1:])
