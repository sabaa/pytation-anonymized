def zip_longest_func():
    from itertools import zip_longest
    a = [1, 2, 3]
    b = [4, 5]
    return list(zip_longest(a, b))


def zip_func():
    a = [1, 2, 3]
    b = [4, 5]
    return list(zip(a, b))


def filter_func():
    a = [1, 2, 3]
    return list(filter(lambda x: x > 1, a))


def map_func():
    a = [1, 2, 3]
    return list(map(lambda x: x + 1, a))


def remove_func():
    a = [1, 2, 3]
    a.remove(2)
    return a


def pop_func():
    a = [1, 2, 3]
    a.pop(1)
    return a


def sort_func():
    a = [1, 3, 2]
    a.sort()
    return a


def sorted_func():
    a = [1, 3, 2]
    return sorted(a)


def extend_func():
    a = [1, 2, 3]
    a.extend([4, 5])
    return a


def append_func():
    a = [1, 2, 3]
    a.append(4)
    return a


def deep_copy_func():
    from copy import deepcopy
    a = [1, 2, 3]
    b = deepcopy(a)
    return b


def copy_func():
    a = [1, 2, 3]
    b = a.copy()
    return b


def isinstance_func():
    a = 1
    return isinstance(a, int)


def issubclass_func():
    class A:
        pass

    class B(A):
        pass

    return issubclass(B, A)


def isnumeric_func():
    a = '1'
    return a.isnumeric()


def isdecimal_func():
    a = '1'
    return a.isdecimal()


def isdigit_func():
    a = '1'
    return a.isdigit()
