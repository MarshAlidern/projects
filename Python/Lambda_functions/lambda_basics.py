x = lambda a : a + 10  #lambda arguments : expression
print(x(5))

x = lambda a, b : a * b #There can be any amount of arguments, but only one expression
print(x(5, 6)) 

x = lambda a, b, c : a + b + c
print(x(5, 6, 2)) 

def myfunc(n):              #we can use lambda functions inside another functions
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))

def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))