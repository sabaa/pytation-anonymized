class Parent1:
    def __init__(self):
        self.msg = "Initializing Parent 1"


class Parent2:
    def __init__(self):
        self.msg = "Initializing Parent 2"


class Child(Parent1, Parent2):
    def __init__(self):
        self.msg = "Initializing Child"
        super().__init__()


def func():
    obj = Child()
    return obj.msg
