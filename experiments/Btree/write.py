from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
import transaction

# Create a new storage file
storage = FileStorage.FileStorage('data/mydata.fs')

# Create a new database using the storage file
db = DB(storage)

# Open a new connection to the database
connection = db.open()

# Get the root of the database
root = connection.root

# Add a BTree to the root of the database
root.btree = OOBTree()

# Add some string keys with associated values
root.btree.update({
    'apple':
    'A sweet, edible fruit produced by an apple tree.',
    'banana':
    'An elongated, edible fruit produced by several kinds of large herbaceous flowering plants.',
    'cherry':
    'A small, round stone fruit that is typically bright or dark red.',
    'date':
    'The sweet, edible fruit of the date palm tree.',
    'elderberry':
    'The berry of the elder tree, used for making wines, liqueurs, and jams.'
})

# Commit the transaction to save changes
transaction.commit()

# Print the value associated with the key 'banana'
print(
    root.btree['banana']
)  # prints: 'An elongated, edible fruit produced by several kinds of large herbaceous flowering plants.'

# Close the connection
connection.close()

# Close the database
db.close()

# Close the storage
storage.close()
