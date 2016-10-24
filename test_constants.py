import subprocess


contents = """
import numpy as np
r = {}
b = 1024 / 2 / r

# do these primes need to be random? I suspect they just need to be really big
p1 = 1000000007 # p1 > n.
p2 = 1000000007 # p2
shingle_hashes = None
signature_hashes = None

np.random.seed({})
num_hashes = r*b
a_params = np.random.randint(low=1, high=p1, size=(num_hashes,1))
b_params = np.random.randint(low=0, high=p1, size=(num_hashes,1))
shingle_hashes = np.concatenate([a_params, b_params], axis=1)
a_params = np.random.randint(low=1, high=p2, size=(num_hashes,1))
b_params = np.random.randint(low=0, high=p2, size=(num_hashes,1))
signature_hashes = np.concatenate([a_params, b_params], axis=1)
"""
with open("out.csv", "w") as results:
    for r in range(10,40):
        for seed in [123, 456, 789, 37, 4, 8, 15, 16, 23, 42]:

            with open("constants.py", "w") as f:
                f.write(contents.format(r, seed))
            
            process = subprocess.Popen(["python2", "runner.py", "and_or.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()

            err = err[err.find("TP=")+3:]
            tp = int(err[:err.find(",")])
            err = err[err.find("FP=")+3:]
            fp = int(err[:err.find(",")])
            err = err[err.find("FN=")+3:]
            fn = int(err[:err.find("\n")])
            
            err = err[err.find("Precision: ")+11:]
            precision = float(err[:err.find(",")])
            err = err[err.find("recall: ")+8:]
            recall = float(err[:err.find(",")])

            f1 = float(out)
            
            b = 1024 / 2 / r
            results.write("{} {} {}, {}, {}, {}, {}, {}\n".format(r, b, tp, fp, fn, precision, recall, f1))
            print("{}	{}	{}	{}	{}	{}	{}	{}".format(r, b, tp, fp, fn, precision, recall, f1))

