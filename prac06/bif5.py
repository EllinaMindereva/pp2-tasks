a = list(input().split())
n = len(a)
for i, j in zip(range(1, n + 1), a):
    print(f"{i} - {j}")