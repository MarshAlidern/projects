numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

a = [1, 2, 3, 4, 5, 6]
e = list(filter(lambda x: x % 2 == 0, a))
print(e)

a = [12, 65, 54, 39, 102, 339, 221, 50, 70]
res = list(filter(lambda x: (x % 13 == 0), a))
print(res)

s = ["geeks", "geeg", "keek", "practice", "aa"]
res = list(filter(lambda x: (x == "".join(reversed(x))), s))
print(res)

from collections import Counter  

s = ["geeks", "geeg", "keegs", "practice", "aa"]
ts = "eegsk"
res = list(filter(lambda x: (Counter(ts) == Counter(x)), s))
print(res)