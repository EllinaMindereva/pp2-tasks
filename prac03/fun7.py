def fun(greeting, *names):
    for name in names:
        print(greeting, name)
fun("Hello", "Ellina", "Lena", "Diyar", "Tair")