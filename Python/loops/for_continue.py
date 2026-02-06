a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in a:
    for num in row:
        if num == 3:
            continue
        print(num, end=" ")

for char in "Pepsi-Cola":
    if char == "e":
        continue
    print(char, end=" ")

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)
