class Student:
    def __init__(self, name):
        self.name = name


def get_obj_name(obj):
    return obj.name


def func():
    student = Student("John")
    student.get_name = get_obj_name
    name = student.get_name(student)
    return name
