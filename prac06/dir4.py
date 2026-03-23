import os
for i in os.scandir("."):
    print(i.name)