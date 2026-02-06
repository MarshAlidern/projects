for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!") 

a = [1, 3, 5, 7, 9, 11]
val = 7
for i in a:
    if i == val:
        print(f"Found at {i}!")
        break
else:
    print(f"not found")

for i in range(10):
    print(i)
    if i == 6:
        break
