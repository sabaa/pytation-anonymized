def func(val1, val2=2):
    return val1 + val2


def call_func():
    res1 = func(1, 2)
    res2 = func(1)
    res3 = func(val1=1)
    res4 = func(val2=1, val1=1)
    return res1, res2, res3, res4
