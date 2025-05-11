class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_age(self):
        return self.age


def func():
    student = Student("John", 20)
    student.grade = 90
    age = student.get_age()
    return student.grade
