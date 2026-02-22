import datetime
x = datetime.datetime.now()
n = x.replace(microsecond = 0)
print(n)