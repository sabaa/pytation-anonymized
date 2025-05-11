class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def func():
    student = Student("John", 20)
    name = student.name
    return name
