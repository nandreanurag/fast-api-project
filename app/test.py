# class MyClass:
#     class_variable = 0  # Class-level variable
#
#     def __init__(self, instance_variable):
#         self.instance_variable = instance_variable  # Instance-level variable
#
#     @classmethod
#     def update_class_variable(cls, new_value):
#         cls.class_variable = new_value
#         print(f"Class variable updated to {new_value}")
#
#     def print_variables(self):
#         print(f"Instance variable: {self.instance_variable}")
#         print(f"Class variable: {MyClass.class_variable}")
#
# # Creating instances of MyClass
# obj1 = MyClass(5)
# obj2 = MyClass(10)
# print(obj1.class_variable)
# # Accessing and printing variables
# obj1.print_variables()
# obj2.print_variables()
#
# # Using the class method to update the class variable
# MyClass.update_class_variable(15)
# # obj1.class_variable=15
# # MyClass.class_variable=15
# # print(MyClass.class_variable)
# # Accessing and printing variables again
# obj1.print_variables()
# obj2.print_variables()
# obj1.class_variable = 10
# print(obj1.class_variable) # an field of class-variable is created in instance
# print(obj2.class_variable) # will display class_variable value
# class Human(object):
#     # A class attribute. It is shared by all instances of this class
#     species = "H. sapiens"
#
#     def __init__(self, name):
#         # Assign the argument to the instance's name attribute
#         self.name = name
#
#         # Initialize property
#         self.age = 0
#
#     def say(self, msg):
#         return "{0}: {1}".format(self.name, msg)
#
#     @classmethod
#     def get_species(cls):
#         return cls.species
#
#     @staticmethod
#     def grunt():
#         return "*grunt*"
#
#     @property
#     def age(self):
#         return self.age
#
#     # This allows the property to be set
#     @age.setter
#     def age(self, age):
#         self.age = age
#
#     # This allows the property to be deleted
#     @age.deleter
#     def age(self):
#         del self.age
#
# d = Human(name="Soeb")
# print (d.say("hi"))  # prints out "Ian: hi"
#
# a = Human("Ameya")
# print (a.say("hello"))  # prints out "Joel: hello"
# a.get_species()  # => "H. sapiens"
from itertools import count
from functools import reduce

from itertools import count
from functools import reduce

def square_numbers():
    for i in count():
        yield i*i

# Generate squares less than 100
squares = square_numbers()
print(list(filter(lambda _: _ < 100, squares)))
# Sum of squares less than 100 using reduce and filter
#result = reduce(lambda x, y: x + y, filter(lambda _: _ < 100, squares))

#print(result)


