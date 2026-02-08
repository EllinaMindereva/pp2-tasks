class Person:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age

p1 = Person("Elya")
p2 = Person("Globus", 2)

print(p1.name, p1.age)
print(p2.name, p2.age)
# init is used to assign values to object properties, or to perform operations that are necessary when the object is being created