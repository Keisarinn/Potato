
import numpy as np
r = 10
b = 1024 / 2 / r

# do these primes need to be random? I suspect they just need to be really big
p1 = 1000000007 # p1 > n.
p2 = 1000000007 # p2
shingle_hashes = None
signature_hashes = None

np.random.seed(42)
num_hashes = r*b
a_params = np.random.randint(low=1, high=p1, size=(num_hashes,1))
b_params = np.random.randint(low=0, high=p1, size=(num_hashes,1))
shingle_hashes = np.concatenate([a_params, b_params], axis=1)
a_params = np.random.randint(low=1, high=p2, size=(num_hashes,1))
b_params = np.random.randint(low=0, high=p2, size=(num_hashes,1))
signature_hashes = np.concatenate([a_params, b_params], axis=1)
