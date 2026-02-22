n = int(input())
def gen(n):
    for i in range(n, -1, -1):
        yield i
print(*gen(n))