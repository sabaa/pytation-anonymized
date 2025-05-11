def func_with_multiple_returns(val):
    return val + 1, 'hello', [2, 3]


def caller():
    a, b, c = func_with_multiple_returns(4)
    return a, b, c
