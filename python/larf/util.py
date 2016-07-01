import re
import numbers
import larf.units

    
def get_method(dotname):
    modname,methname = dotname.rsplit('.',1)
    import importlib
    mod = importlib.import_module(modname)
    return getattr(mod, methname)

def listify(string, delim=', '):
    return [x for x in re.split('['+delim+']', string) if x]



def unit_dict():
    ret = dict()
    for k,v in larf.units.__dict__.items():
        if k.startswith('_'):
            continue
        ret[k] = v
    return ret

def unitify(expression, **variables):
    "Return expression string as numeric value resolving units."
    if expression is None:
        return None
    if isinstance(expression, numbers.Number):
        return expression
    try:
        ret = eval(expression, unit_dict(), variables)
    except NameError:
        return expression
    return ret

def unit_eval(kwds, **variables):
    "Return dictionary made by evaulating the given kwds dict values for units and other variables."
    ret = dict()
    for k,v in kwds.items():
        ret[k] = unitify(v, **variables)
    return ret


def expand_range_dict(d):
    "Expand a dictionary with keys that are either integers, lists of integers of 2-tuple of integers (ranges)"
    ret = dict()
    for k,v in d.items():
        if isinstance(k, numbers.Number):
            ret[k] = v
            continue
        if isinstance(k, tuple):
            for ind in range(*k):
                ret[ind] = v
            continue
        for ind in k:
            ret[ind] = v
    return ret

def expand_tuple_list(d):
    "Expand a list of tuples like [((1,10),100), (11,200)] to dictionary keyed by that first number"
    ret = dict()
    for k,v in d:
        if isinstance(k, numbers.Number):
            ret[k] = v
            continue
        if isinstance(k, tuple):
            start,stop = k
            for ind in range(start, stop+1):
                ret[ind] = v
            continue
        for ind in k:
            ret[ind] = v
    return ret
