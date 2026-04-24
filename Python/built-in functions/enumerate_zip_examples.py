fruits = ["apple", "banana", "cherry"]
colors = ["red", "yellow", "dark red"]

for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)

for fruit, color in zip(fruits, colors):
    print(f"{fruit} is {color}")