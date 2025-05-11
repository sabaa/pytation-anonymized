class Parent1:
    def method(self):
        return "Method from Parent 1"


class Parent2:
    def method(self):
        return "Method from Parent 2"


class Child(Parent2, Parent1):
    def method(self):
        return super().method() + " (Child)"


def func():
    obj = Child()

    result = obj.method()
    return result
