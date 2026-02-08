words = ["ford", "mustang", "is", "my", "favourite", "car"]
sortwords = sorted(words, key=lambda a: len(a))
print(sortwords)
# sorted() can use a lambda as a key for custom sorting