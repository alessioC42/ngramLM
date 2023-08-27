import database
from sys import argv

filename = argv[1]
N        = argv[2]
count    = argv[3]
query    = argv[4:]


DB = database.Database(filename, int(N))

print(DB.query(query, int(count)))