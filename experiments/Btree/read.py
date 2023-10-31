from ZODB import FileStorage, DB
import transaction

# Open the existing storage file
storage = FileStorage.FileStorage('data/mydata.fs')

# Open the existing database using the storage file
db = DB(storage)

# Open a new connection to the database
connection = db.open()

# Get the root of the database
root = connection.root

# Access the BTree from the root of the database
btree = root.btree

# Print all keys and their associated values in the BTree
for key, value in btree.items():
    print(f'{key}: {value}')

# Close the connection
connection.close()

# Close the database
db.close()

# Close the storage
storage.close()
