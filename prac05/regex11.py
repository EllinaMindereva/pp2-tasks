import re
s = input()
x = re.findall(r"a\S*b", s)
print(x)
