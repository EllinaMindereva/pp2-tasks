a = list(map(int, input().split()))
b = list(filter(lambda x: x % 9 == 0, a))
print(*b)