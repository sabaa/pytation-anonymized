def multiple_iterator():
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = {}
    for key, value in dict1.items():
        dict2[key] = value**2
    return dict2

