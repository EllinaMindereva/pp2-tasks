import functools
a = list(map(int, input().split()))
b = functools.reduce(lambda x, y: x + y, a)
print(b)