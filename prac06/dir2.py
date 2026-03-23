import os
for i in os.listdir():
    if os.path.isfile(i):
        print(f"{i} - file")
        print("---")
    elif os.path.isdir(i):
        print(f"{i} - folder")
        print("---")