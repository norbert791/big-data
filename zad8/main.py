from random import uniform
from scipy.spatial.distance import euclidean
from numpy import mean, std, array

def randomPoint(n: int):
    return tuple(map(lambda _: uniform(0, 1), range(n)))

def dm2(k:int, n: int):
    maxDist = 0
    minDist = 0
    points = list(map(lambda _: randomPoint(n), range(k)))
    
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue
            dist = euclidean(p1, p2)
            if dist > maxDist:
                maxDist = dist
            if minDist == 0 or minDist > dist:
                minDist = dist
    
    return maxDist / minDist

if __name__ == "__main__":
    samples = 50
    k = 50
    nls = [10**k for k in range(5)]
    
    for n in nls:
        results = map(lambda _:dm2(k,n), range(samples))
        results = array(list(results))
        print(f"n: {n}, mean: {mean(results)}, std: {std(results)}")