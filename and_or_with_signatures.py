# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 17:32:29 2016

@author: Daniel Keyes, Siggi
"""

import numpy as np


import_constants = False
check_similarity = True
check_signitures = False
if import_constants:
    # this module is generated programmatically, for testing
    import constants
    
    r = constants.r
    b = constants.b
    p1 = constants.p1
    p2 = constants.p2
    hashes = constants.hashes
else:
    # Not sure how the 1024 hash-limit is checked/imposed. If we have b bands with
    # r rows each, then we need r*b shingle hashes and b signature hashes (which
    # internally compute r hashes)
    # Does that count as 1024 >= r*b + b? 1024 >= 2*r*b? 1024 >= 2*r*b + b? not sure
    # This is an approximate solution to 2*r*b = 1024 and (1/b)^(1/r) = 0.85 according to wolfram:
    r = 20
    b = 51

    # do these primes need to be random? I suspect they just need to be really big
    p1 = 1000000007 # p1 > n.
    p2 = 1000000007 # p2
    p3 = 8209
    hashes = None

    np.random.seed(123)
    num_hashes = r*b
    a_params = np.random.randint(low=1, high=n, size=(num_hashes,1))
    b_params = np.random.randint(low=0, high=n, size=(num_hashes,1))
    hashes = np.concatenate([a_params, b_params], axis=1)

n = 8192 # num shingles
    
def min_hash(shingles):
    global p1, n, hashes
    shingles = np.asarray(shingles)
    result = []
    for i in range(hashes.shape[0]):
        min_value = np.min((shingles*hashes[i,0] + hashes[i,1])  % p3)
        result.append(min_value)
    return result

def hash_bands(signature):
    global r, b, p2, hashes
    result = []
    for i in range(b):
        h = 0
        for j in range(i*r, (i+1)*r):
            # re-use hashes for the band hash. ideally, computing a random
            # hash twice is still a random hash.
            h += (signature[j]*hashes[j,0] + hashes[j,1]) % p2
        result.append(h % p2)
    return result
    
def mapper(key, value):
    # key: None
    # value: one line of input file
    tokens = value.split()
    name = int(tokens[0].split("_")[1])
    shingles = [int(i) for i in tokens[1:]]
    
    and_hash = min_hash(shingles)
    or_hash = hash_bands(and_hash)
    
    global check_similarity
    if check_similarity:
        value = (name, set(shingles))
    elif check_signitures:
        value = (name,and_hash)
    else:
        value = name
    global p2
    for band, or_bucket in enumerate(or_hash):
        yield band*p2 + or_bucket, value

def reducer(key, values):
    global check_similarity
    global check_signitures
    # key: key from mapper used to aggregate
    # values: list of all value for that key
    if check_similarity:
        for (i, s1) in values:
            for (j, s2) in values:
                if i >= j:
                    continue
                intersection = len(s1.intersection(s2))
                union = len(s1.union(s2))
                similarity = float(intersection)/union
                if similarity >= 0.85:
                    yield i, j
    elif check_signitures:
        for (i, s1) in values:
            for (j, s2) in values:
                if i >= j:
                    continue
                intersection = sum(1 for i, j in zip(s1, s2) if i == j)
                jacc = float(intersection)/(r*b)    
                if jacc > 0.85:
                    yield i, j
    else:
        for i in values:
            for j in values:
                if i >= j:
                    continue
                yield i, j
