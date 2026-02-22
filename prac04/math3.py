import math
n = int(input())
a = int(input())
p = math.pi
rad = math.radians(180/n)
h = a / (2 * math.tan(rad))
area = (n * a * h) / 2
print(round(area))