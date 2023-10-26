import shelve
from term import TermInfo

# Open a shelf file. The 'c' option means to open the file for reading and writing, creating it if it does not exist.
shelf = shelve.open('all.db', 'c')

str1 = 'hello'
str2 = 'world'
str3 = 'hola'
str4 = 'munod'

# Store your data in the shelf.
shelf[str1] = TermInfo(3, [4, 1])
shelf[str2] = TermInfo(2, [4, 2])
shelf[str3] = TermInfo(1, [4, 0])
shelf[str4] = TermInfo(0, [4, 0])

# Always remember to close the shelf file when you're done with it.
shelf.close()
