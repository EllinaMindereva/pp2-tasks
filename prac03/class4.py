class Person:
  def __init__(self, name):
    self.name = name

  def printname(self):
    print(self.name)

p1 = Person("Lena")
p2 = Person("Dayana")

p1.printname()
p2.printname()
# self is used to access properties and methods that belong to the class