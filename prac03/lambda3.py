def fun(n):
    return lambda a: a * n
three = fun(3) # multiply a and 3
five = fun(5) # multiply a and 5
print(three(9)) 
print(five(9))
# return both