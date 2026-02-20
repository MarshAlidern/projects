students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

a = [(2, 'B'), (1, 'A'), (3, 'C')]
b = sorted(a, key=lambda x: x[0])
print(b)

a = [(3, 'fun!'), (1, 'Python'), (2, 'is')]
sorted_data = sorted(a, key=lambda x: x[0])
print(sorted_data)

a = [(3, 'fun!'), (1, 'Python'), (2, 'is')]
sorted_data = sorted(a, key=lambda x: x[0], reverse=True)
print(sorted_data)