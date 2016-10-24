import numpy as np


import_constants = False
check_similarity = False

if import_constants:
    # this module is generated programmatically, for testing
    import constants
    
    r = constants.r
    b = constants.b
    p1 = constants.p1
    p2 = constants.p2
    shingle_hashes = constants.shingle_hashes
    signature_hashes = constants.signature_hashes
else:
    # Not sure how the 1024 hash-limit is checked/imposed. If we have b bands with
    # r rows each, then we need r*b shingle hashes and b signature hashes (which
    # internally compute r hashes)
    # Does that count as 1024 >= r*b + b? 1024 >= 2*r*b? 1024 >= 2*r*b + b? not sure
    # This is an approximate solution to 2*r*b = 1024 and (1/b)^(1/r) = 0.85 according to wolfram:
    r = 23
    b = 22

    # do these primes need to be random? I suspect they just need to be really big
    p1 = 1000000007 # p1 > n.
    p2 = 1000000007 # p2
    shingle_hashes = None
    signature_hashes = None

    np.random.seed(123)
    num_hashes = r*b
    a_params = np.random.randint(low=1, high=p1, size=(num_hashes,1))
    b_params = np.random.randint(low=0, high=p1, size=(num_hashes,1))
    shingle_hashes = np.concatenate([a_params, b_params], axis=1)
    a_params = np.random.randint(low=1, high=p2, size=(num_hashes,1))
    b_params = np.random.randint(low=0, high=p2, size=(num_hashes,1))
    signature_hashes = np.concatenate([a_params, b_params], axis=1)

n = 8192 # num shingles
    
def min_hash(shingles):
    global p1, n, shingle_hashes
    shingles = np.asarray(shingles)
    result = []
    for i in range(shingle_hashes.shape[0]):
        min_value = np.min(((shingles*shingle_hashes[i,0] + shingle_hashes[i,1]) % p1) % n)
        result.append(min_value)
    return result

def hash_bands(signature):
    global r, b, p2, signature_hashes
    result = []
    for i in range(b):
        h = 0
        for j in range(i*r, (i+1)*r):
            h += (signature[j]*signature_hashes[j,0] + signature_hashes[j,1]) % p2
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
    else:
        value = name
    global p2
    for band, or_bucket in enumerate(or_hash):
        yield band*p2 + or_bucket, value

def reducer(key, values):
    global check_similarity
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
    else:
        for i in values:
            for j in values:
                if i >= j:
                    continue
                yield i, j
