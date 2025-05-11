def func():
    dict1 = {'a': 'b', 'b': 'c', 'c': 'a'}
    list1 = []
    for key, value in dict1.items():
        list1.append(','.join([key, value]))
    return list1[0]
