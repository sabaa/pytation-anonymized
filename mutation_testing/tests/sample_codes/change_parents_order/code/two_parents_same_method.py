class Parent1:
    parameter1 = 1

    def method(self):
        return "Method from Parent 1 parameter: {}.".format(self.parameter1)


class Parent2:
    parameter2 = 2

    def method(self):
        return "Method from Parent parameter: {}.".format(self.parameter2)


class Child(Parent1, Parent2):
    pass


def func():
    obj = Child()

    result = obj.method()
    return result
