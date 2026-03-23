with open("exercise.txt", "a") as f:
    f.write("\nHi")
with open("exercise.txt") as f:
    print(f.read())