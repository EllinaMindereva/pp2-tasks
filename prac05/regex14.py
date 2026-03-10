import re
s = input()
x = re.findall(r"^[a-z]+|[A-Z][a-z]*", s)
print(x)