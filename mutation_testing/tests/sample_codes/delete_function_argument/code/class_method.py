class SomeClass:
    def __init__(self, arg1, arg2=3):
        self.arg1 = arg1
        self.arg2 = arg2

    def some_method(self, arg3=4):
        return self.arg1 + self.arg2 + arg3

    @staticmethod
    def some_static_method(arg1, arg2=3):
        return arg1 + arg2

    @classmethod
    def some_class_method(cls, arg1, arg2=3):
        return arg1 + arg2


def call_some_method():
    obj = SomeClass(2, 1)
    res1 = obj.some_method(5)
    res2 = SomeClass.some_static_method(2, 1)
    res3 = SomeClass.some_class_method(2, 1)
    return res1, res2, res3
