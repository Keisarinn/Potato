
def mapper(key, value):
    yield 1, value

def reducer(key, values):
    # naive: compare all videos in O(n^2)
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
        
