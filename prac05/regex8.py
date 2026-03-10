import re
s = input()
x = re.findall(r"abbb?", s)
print(x)