i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1 

i = 0
a = 'pepsi-cola'
while i < len(a):
    if a[i] == 'e' or a[i] == 's':
        i += 1
        break   
    print(a[i])
    i += 1

cnt = 5
while True:
    print(cnt)
    cnt -= 1
    if cnt == 0:
        print("Countdown finished!")
        break
