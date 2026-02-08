nums = [1, 2, 6, 7, 9, 12, 17, 19, 20, 52]
even = list(filter(lambda a: a % 2 == 0, nums))
print(even)
# filter() creates a list of items for which a function returns True