from config import RANGES

def normalize(value, key):
    xmin, xmax = RANGES[key]

    value = max(min(value, xmax), xmin)

    if xmax == xmin:
        return 0

    return round(100 * (value - xmin) / (xmax - xmin), 2)


def normalize_all(features):
    return {
        key: normalize(val, key)
        for key, val in features.items()
    }