import datetime
h1, m1, s1 = list(map(int, input().split()))
h2, m2, s2 = list(map(int, input().split()))
a = datetime.timedelta(hours = h1, minutes = m1, seconds = s1)
b = datetime.timedelta(hours = h2, minutes = m2, seconds = s2)
dif = abs((a - b).total_seconds())
print(dif)