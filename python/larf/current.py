from larf.vector import Scalar
from larf.util import mgrid_to_linspace
import math
import numpy

def sample(steps, cfield, mgrid, lcar = None, **kwds):
    '''
    Sample current field cfield along steps at a granularity near lcar.

    If lcar not given divine it based on mgrid.

    Return an array of 5-arrays: (x,y,z,time,current)
    '''
    import larf.util
    linspaces = mgrid_to_linspace(mgrid)
    curfield = Scalar(cfield, linspaces)

    if not lcar:
        lcar = min(linspaces[0][1] - linspaces[0][0],
                   linspaces[1][1] - linspaces[1][0],
                   linspaces[2][1] - linspaces[2][0])

    result = list()
    for istep, p1 in enumerate(steps[:-1]):
        p2 = steps[istep+1]
        step = p2-p1
        dist = math.sqrt(numpy.dot(step[:3], step[:3]))
        n = max(2, int(dist/lcar))
        for count in range(n):
            p = p1 + float(count)/float(n)*step
            r = p[:3]
            cur = curfield(r)
            pw = numpy.hstack((p, cur))
            result.append(pw)
    ret = numpy.asarray(result)

    return ret

def differential(weighting, p1, p2):
    q1 = weighting(p1[:3])
    q2 = weighting(p2[:3])
    return (q2-q1)/(p2[3]-p1[3])
    

def stepwise(weighting, path, charge=1.0):
    '''
    Sample weighting potential around each of the 4-points (x,y,z,t)
    in path returning array of corresponding currents in units of
    charge/time
    '''
    samples = list()

    halvsies = [0.5*(a+b) for a,b in zip(path[:-1], path[1:])]
    for left, center, right in zip([None]+halvsies, path, halvsies+[None]):
        cur = list()
        if left is not None:
            cur.append(charge * differential(weighting, left, center))
        if right is not None:
            cur.append(charge * differential(weighting, center, right))
        samples.append(sum(cur)/len(cur))
    return numpy.asarray(samples)
