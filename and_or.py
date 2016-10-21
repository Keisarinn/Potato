import numpy as np

# Not sure how the 1024 hash-limit is checked/imposed. If we have b bands with
# r rows each, then we need r*b shingle hashes and b signature hashes (which
# internally compute r hashes)
# Does that count as 1024 >= r*b + b? 1024 >= 2*r*b? 1024 >= 2*r*b + b? not sure
# This is an approximate solution to 2*r*b = 1024 and (1/b)^(1/r) = 0.85 according to wolfram:
r = 20
b = 24

n = 10000 # num shingles
m = 10 # num buckets for each band
# do these primes need to be random?
p1 = 10007 # p1 > n.
p2 = 1009 # p2 > m
shingle_hashes = None
signature_hashes = None

def init_hashes():
    global r, b, p1, p2, shingle_hashes, signature_hashes
    np.random.seed(12345)
    num_hashes = r*b
    a_params = np.random.randint(low=1, high=p1, size=(num_hashes,1))
    b_params = np.random.randint(low=0, high=p1, size=(num_hashes,1))
    shingle_hashes = np.concatenate([a_params, b_params], axis=1)
    a_params = np.random.randint(low=1, high=p2, size=(num_hashes,1))
    b_params = np.random.randint(low=0, high=p2, size=(num_hashes,1))
    signature_hashes = np.concatenate([a_params, b_params], axis=1)
    
def compute_hash(shingles, hashes, p, N):
    result = []
    for shingle in shingles:
        min_value = np.min(((shingle * hashes[:,0] + hashes[:,1]) % p) % N)
        result.append(min_value)
    return result

def hash_doc(shingles):
    global p1, n, shingle_hashes
    return compute_hash(shingles, shingle_hashes, p1, n)

def hash_bands(signature):
    global r, b, p2, m, signature_hashes
    result = []
    for i in range(b):
        band = range(i*r, (i+1)*r)
        h = sum(compute_hash(signature, signature_hashes[band,:], p2, m))%m
        result.append(h)
    return result
    
def mapper(key, value):
    if shingle_hashes is None:
        init_hashes()
    # key: None
    # value: one line of input file
    tokens = value.split()
    name = tokens[0]
    shingles = [int(i) for i in tokens[1:]]
    
    and_hash = hash_doc(shingles)
    or_hash = hash_bands(and_hash)
    #print("[map] {}".format(name))
    #print("[map] {}: {}".format(name, shingles))
    #print("[map] and: {}".format(and_hash))
    #print("[map] or: {}".format(or_hash))
    
    global m
    for band, or_bucket in enumerate(or_hash):
        yield band*m + or_bucket, value

def reducer(key, values):
    # key: key from mapper used to aggregate
    # values: list of all value for that key
    #print("[reduce] {}: {}".format(key, values))
    #print("[reduce] {}. checking {} documents via pairwise comparisons".format(key, len(values)))
    videos = {}
    for value in values:
        tokens = value.split()
        name = int(tokens[0].split("_")[1])
        shingles = [int(i) for i in tokens[1:]]
        videos[name] = shingles
    for i in videos:
        s1 = set(videos[i])
        for j in videos:
            if i >= j:
                continue
            s2 = set(videos[j])
            intersection = len(s1.intersection(s2))
            union = len(s1.union(s2))
            similarity = float(intersection)/union
            #print("similarity of ({},{}): {}/{} = {}".format(i, j, intersection, union, similarity))
            if similarity >= 0.85:
                yield i, j
        
