def func(val1, val2=2, val3=3):
    return val1 + val2 + val3


def call_func():
    res1 = func(1, 1, 1)
    res2 = func(1)
    res3 = func(val2=4, val1=1)
    return res1, res2, res3
