import shelve

# Open a shelf file. The 'c' option means to open the file for reading and writing, creating it if it does not exist.
indexes = shelve.open('indexes.db', 'c')
values = shelve.open('values.db', 'c')
shelf = shelve.open('all.db', 'c')

# Store your data in the shelf.
idx: list[int] = []


def random(i: int) -> str:
    return 'random' + str(i)


# List of string with numbers up to 10000
numbers: list[str] = [str(i) for i in range(100000)]

for i in range(100000):
    print(i)
    idx.append(i)
    indexes[numbers[i]] = idx[i]
    values[str(i)] = random(i)

for number in numbers:
    shelf[number] = random(int(number))

# Always remember to close the shelf file when you're done with it.
shelf.close()
