from functools import reduce

nums = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x**2, nums))
print("Squares:", squares)

evens = list(filter(lambda x: x % 2 == 0, nums))
print("Evens:", evens)

product = reduce(lambda x, y: x * y, nums)
print("Product of numbers:", product)