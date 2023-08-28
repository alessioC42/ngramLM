import database
from sys import argv

filename = argv[1]
N        = argv[2]
count    = argv[3]
ran_query= bool(argv[4])
query    = argv[5:]


DB = database.Database(filename, int(N), random_query=ran_query)

print(DB.query(query, int(count)))
