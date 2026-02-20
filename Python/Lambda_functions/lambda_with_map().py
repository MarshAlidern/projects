numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

a = [1, 2, 3, 4, 5]
b = map(lambda x: x**2, a)
print(list(b))

a = [1, 2, 3]
b = [4, 5, 6]
c = map(lambda x, y: x + y, a, b)
print(list(c))

a = ["apple", "banana", "cherry"]
b = map(lambda x: x.upper(), a)
print(list(b))

a = [1, 2, 3, 4, 5]
multiplied = map(lambda x: x * 3, a)
print(list(multiplied))