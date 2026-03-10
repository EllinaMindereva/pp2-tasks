import re
s = input()
x = re.sub(r"([A-Z])", r" \1", s)
print(x)