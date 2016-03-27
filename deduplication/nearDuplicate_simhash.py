#!/usr/bin/env python2.7  

from __future__ import division
import sys
import re
from binascii import crc32
import itertools

max_shingle_id = 2**32 - 1

# Length of our simhash value
hashbits = 32

def get_shingles(image, k):
    shingles = set([image[i: i + k] for i in range(0, len(image) - k)])

    # Maps shingles to id that is 32-bit integer                                                                                                   
    shingles_id = set([crc32(x) & 0xffffffff for x in shingles])
    return shingles_id

def get_fingerprint(shingles):
    v = [0] * hashbits
    for id in shingles:
        for i in xrange(hashbits):
            bitmask = 1 << i
            if id & bitmask:
                v[i] += 1
            else:
                v[i] -= 1
    fingerprint = 0
    for i in xrange(hashbits):
        if v[i] >= 0:
            fingerprint = fingerprint | (1 << i)
    return fingerprint
    
def hamming(a, b):
    x = (a ^ b) & ((1 << hashbits) - 1)
    dist = 0
    while x:
        dist += 1
        x = x & (x - 1)
    return dist


def computeSimhash(images, threshold=0.8, k=3):
    fingerprints = {}
    
    for key, value in images.iteritems():
        shingles = get_shingles(value, k)
        
        fingerprints[key] = get_fingerprint(shingles)
    
    similar = []
    for pair in itertools.combinations(fingerprints.keys(), 2):
        fingerprint1 = fingerprints[pair[0]]
        fingerprint2 = fingerprints[pair[1]]
        similarity = 1 - hamming(fingerprint1, fingerprint2) / hashbits
        
        if similarity >= threshold:
            similar.append(pair)
    
    return similar


def jaccard(a, b):
    intersection = set(a) & set(b)
    union = set(a) | set(b)
    
    return len(intersection) / len(union)

if __name__ == '__main__':
    if (len(sys.argv) != 5):
        print 'Usage: %s <path to dump file> <path to created ouput file> <k> <threshold>' % (sys.argv[0])
        sys.exit(-1)

    from common import readDump

    file_path = sys.argv[1]
    images = readDump(file_path)
    
    k = int(sys.argv[3])
    threshold = float(sys.argv[4])
    
    similar = computeSimhash(images, threshold, k)
    near_duplicates = []
    
    for pair in similar:
        value1 = images[pair[0]] 
        shingles1 = set([value1[i: i + k] for i in range(0, len(value1) - k)])
        
        value2 = images[pair[1]] 
        shingles2 = set([value2[i: i + k] for i in range(0, len(value2) - k)])

        if jaccard(shingles1, shingles2) >= threshold:
            near_duplicates.append(pair)
    
    with open(sys.argv[2], 'w') as output:
        for pair in near_duplicates:
            output.write('%s\n%s\n\n' %(pair[0], pair[1]))
            
    print "Total Images: ", len(images.keys())
    print "Near Duplicates: ", len(near_duplicates)

    
