class Grandparent:
    attribute = "Attribute from Grandparent"

    def method(self):
        return "Method 1 from Grandparent. Attribute: {}.".format(self.attribute)


class Parent1(Grandparent):
    attribute = "Attribute from Parent 1"

    def method(self):
        return "Method 2 from Parent 1. Attribute: {}.".format(self.attribute)


class Parent2(Grandparent):
    def method(self):
        return "Method 3 from Parent 2. Attribute: {}.".format(self.attribute)


class Child(Parent2, Parent1):
    def call_method(self):
        return self.method()


def func():
    obj = Child()
    result = obj.call_method()
    return result
