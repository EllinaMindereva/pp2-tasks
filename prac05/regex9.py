import re
s = input()
x = re.findall(r"[a-z]+_[a-z]+", s)
print(x)