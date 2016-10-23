# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 17:49:00 2016

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
    videos = {}
    for value in values:
        print(value)
        #tokens = value.split()
        name = int(value[0])
        #print(int(tokens[1]))
        videos[name] = value[1:]
    s1 = set(videos[int(key)])
    for i in videos:
        if int(key) != i:
            s2 = set(videos[i])
            intersection = len(s1.intersection(s2))
            union = len(s1.union(s2))
            similarity = float(intersection)/union
            #print("similarity of ({},{}): {}/{} = {}".format(i, j, intersection, union, similarity))
            if similarity >= 0.85:
                yield int(key), i
        

def hashfunction1024(value,size):
    sign = np.zeros([size], dtype='i4')
    rand = randomized(8193,1024)
    for i in range (size):
        temp = np.column_stack((value,rand[:,i]))
        sign[i] = np.argmax(temp[temp[:,1].argsort()][:,0])
    return sign.astype('i4')

def randomized(n,size):
    array = np.zeros([n,size], dtype='i4')
    np.random.seed(500)
    for i in range(size):
        array[:,i] = np.random.permutation(n)
    return array

