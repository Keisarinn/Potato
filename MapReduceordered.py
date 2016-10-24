@author: Siggi
"""
import numpy as np

def mapper(key, value):
    # key: None
    # value: one line of input file
    arr = np.sort(np.asarray(list(set((value.split()[1:]))),dtype=np.int16))
    indexarr = np.zeros([8193], dtype='i4')
    indexarr[arr] = 1
    val = 0
    if ((value.split()[0])[6:].lstrip("0")):
        val = int((value.split()[0])[6:].lstrip("0"))
    #sign =  (np.array_str(hashfunction1024(indexarr,1024)).strip(']')).strip('[')
    sign = np.append(val,hashfunction1024(indexarr,1024))
    #signn = tuple(np.append([int(val)], sign ))  
    for i in range(int(val)+1): 
        yield str(i), sign  # this is how you yield a key, value pair



def reducer(key, values):
    # key: key from mapper used to aggregate
    # values: list of all value for that key
    #print("[reduce] {}: {}".format(key, values))
    #print("[reduce] {}. checking {} documents via pairwise comparisons".format(key, len(values)))
    
    index = [i for i,x in enumerate(values) if int(x[0]) == int(key)]
    #print(index)
    val = (values[index[0]])[1:]
    for value in values:
        if int(value[0]) != int(key):
            #print(np.shape(value[1:]))
            intersection = sum(1 for i, j in zip(value[1:], val) if i == j)
            print(intersection)
            jacc = intersection/(1024)    
            print(jacc)
            if jacc > 0.85:
               yield int(key), int(value[0])


def hashfunction1024(value,size):
    sign = np.zeros([size], dtype='i4')
    rand = randomized(8193,1024)
    for i in range (size):
        temp = np.column_stack((value,rand[:,i]))
        sign[i] = np.argmax(temp[temp[:,1].argsort()][:,0])
    return sign.astype('i4')

def randomized(n,size):
    array = np.zeros([n,size], dtype='i4')
    np.random.seed(20)
    for i in range(size):
        array[:,i] = np.random.permutation(n)
    return array

