#!/usr/bin/env python2.7  

from __future__ import division
import sys
import re
from binascii import crc32
import itertools

max_shingle_id = 2**32 - 1
# Smallest prime greater than max_shingle_id
p = 4294967311

# Number of hash functions used
num_hashes = 200
    
def get_shingles(image, k):
    shingles = set([image[i: i + k] for i in range(0, len(image) - k)])
    
    # Maps shingles to id that is 32-bit integer
    shingles_id = set([crc32(x) & 0xffffffff for x in shingles])
    return shingles_id
    

def pick_random_coeffs(num):
    import random
    
    # Smallest prime greater than max_shingle_id
    ret = []
    while (num > 0):
        rand = random.randint(0, max_shingle_id)
        while (rand in ret):
            rand = random.randint(0, max_shingle_id)

        ret.append(rand)
        num -= 1

    return ret


def computeSignatures(images, k=3):
    # Initializes random hash functions ((a * x + b) % p) % max
    a_coeffs = pick_random_coeffs(num_hashes)
    b_coeffs = pick_random_coeffs(num_hashes)
    
    signatures = {}
    
    for key, value in images.iteritems():
        shingles = get_shingles(value, k)
        
        signature = []
        for i in xrange(0, num_hashes):
            minhash = max_shingle_id + 1
            for shingle in shingles:
                hashed = ((a_coeffs[i] * shingle + b_coeffs[i]) % p) % (max_shingle_id + 1)
                
                if hashed < minhash:
                    minhash = hashed
            signature.append(minhash)
        signatures[key] = signature
    
    return signatures


def getSimilar(signatures, threshold=0.8):
    similar = []

    # Get all possible image pairs
    for pair in itertools.combinations(signatures.keys(), 2):
        same = 0
        
        signature1 = signatures[pair[0]]
        signature2 = signatures[pair[1]]
        for i in xrange(0, num_hashes):
            same += (signature1[i] == signature2[i])
            
        if same / num_hashes >= threshold:
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
    
    signatures = computeSignatures(images, k)
    similar = getSimilar(signatures, threshold)
    
    near_duplicates = []

    # Checks the estimated similarites by computing the actual jaccard distance
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
