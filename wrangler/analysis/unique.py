#!/usr/bin/env python2.7

import sys, getopt
import glob

def getUnique(path):
    files = glob.glob(path + '/*/dump')
    unique = {}
    overlap = 0
    for f in files:
        print "Checking ... ", f
        fileRead = open(f, 'r')
        for line in fileRead:
            if line.startswith('URL'):
                url = line[line.find('::') + 2:].strip()
                while (1):
                    for meta in fileRead:
                        if 'Content-Type' in meta:
                            mime = meta.split('=')[1]
                            if mime.startswith('image'):
                                if unique.get(url,0) == 0:
                                    yield url
                                else:
                                    overlap += 1
                                ## unique |= set(url)
                                unique[url] = unique.get(url, 0) + 1
                            break
                    break
        fileRead.close()
    print "Unique Images: ", len(unique)
    print "Overlap Images: ", overlap

def main(argv=sys.argv):
    usage = "unique.py -i <input> -o <output>"
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

    with open(output, 'w') as f:
        for url in getUnique(input):
            f.write("%s\n" % url)

if __name__ == '__main__':
    main(sys.argv[1:])
