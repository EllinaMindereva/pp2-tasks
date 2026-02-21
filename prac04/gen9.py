n = int(input())
def gen(n):
    for i in range(1, n + 1):
        yield i * i
for i in gen(n):
    print(i)