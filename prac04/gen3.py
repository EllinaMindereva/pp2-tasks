def simple_gen():
  yield "Emir"
  yield "Raim"
  yield "Tair"

gen = simple_gen()
print(next(gen))
print(next(gen))
print(next(gen))
