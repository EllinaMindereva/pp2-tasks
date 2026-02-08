def fun(**v):
    print("Type:", type(v))
    print("Car brand:", v["car"])
    print("Model:", v["model"])
    print("All information:", v)
fun(car = "Ford", model = "Mustang", colour = "Dark blue")