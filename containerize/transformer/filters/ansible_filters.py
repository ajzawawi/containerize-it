def flatten(value):
    if isinstance(value, list):
        return [item for sublist in value for item in (sublist if isinstance(sublist, list) else [sublist])]
    return value

def combine(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return {**a, **b}
    return a

def dict2items(d):
    if isinstance(d, dict):
        return [{"key": k, "value": v} for k, v in d.items()]
    return d

def get_filters():
    return {
        "flatten": flatten,
        "combine": combine,
        "dict2items": dict2items,
    }
