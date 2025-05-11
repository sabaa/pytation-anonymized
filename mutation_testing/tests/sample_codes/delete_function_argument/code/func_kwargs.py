def func(**kwargs):
    if 'a' in kwargs:
        return 'a is found'
    elif 'b' in kwargs:
        return 'b is found'
    return 'neither a nor b is found'


def call_func():
    res1 = func(a=1)
    res2 = func(b=1)
    res3 = func(c=1)
    res4 = func(a=1, b=2)
    res5 = func(b=1, a=2)
    return res1, res2, res3, res4, res5
