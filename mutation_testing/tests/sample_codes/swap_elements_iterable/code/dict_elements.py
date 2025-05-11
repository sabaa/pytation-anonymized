def func():
    dict1 = {'k1': 2, 'k2': 4, 'k3': 5, 'k4': 1, 'k5': 7}

    els = []
    for v in dict1.values():
        if v > 3:
            els.append(v)

    return els[0]
