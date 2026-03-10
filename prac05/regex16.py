import re
s = input()
x = re.sub(r"([A-Z])", lambda match: "_" + match.group(1).lower(), s)
print(x)