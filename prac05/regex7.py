import re
s = input()
x = re.findall(r"ab*", s)
print(x)