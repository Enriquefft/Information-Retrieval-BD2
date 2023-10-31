import shelve

# Open the shelve file
shelf = shelve.open('all.db')

# Iterate over the keys and print the values
for key in shelf:
    value = shelf[key]
    print(f"{key} : {value}")

# Close the shelve file
shelf.close()
