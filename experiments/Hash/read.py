import shelve

# Open the shelve file
shelf = shelve.open('indexes.db')

# Iterate over the keys and print the values
c = 0
for key in shelf:
    if c == 1:
        break
    c = c + 1
    value = shelf[key]
    print(key)
    # print(f"{key}, : , {value}")

# Close the shelve file
shelf.close()
