class Parent1:
    parameter = "parameter 1"

    def method1(self):
        return "Method 1 from parent 1. parameter = {}.".format(self.parameter)


class Parent2:
    parameter = "parameter 2"

    def method2(self):
        return "Method 2 from parent 2. parameter = {}.".format(self.parameter)


class Child(Parent1, Parent2):
    def call_methods(self):
        result1 = self.method1()
        result2 = self.method2()
        return result1, result2


def func():
    obj = Child()
    results = obj.call_methods()
    return results
