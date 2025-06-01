

def unique(value, attribute=None, case_sensitive=False):
    if not isinstance(value, list):
        return value
    
    seen = set()
    result = []
    
    for item in value:
        if attribute and isinstance(item, dict):
            key = item.get(attribute)
        else:
            key = item

        if isinstance(key, str) and not case_sensitive:
            key = key.lower()

        if key not in seen:
            seen.add(key)
            result.append(item)

    return result

def get_filters():
    return {
        # "flatten": flatten,
        # "combine": combine,
        # "dict2items": dict2items,
        "unique": unique
    }
