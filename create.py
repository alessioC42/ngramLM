import database
from string import punctuation
from tqdm import tqdm

DBPATH   = "db.db"
N        = 5

DB = database.Database(DBPATH, N)

import os

dir = "texts"

files = os.listdir(dir)


print(f"{str(len(files))} files to process")
for file in tqdm(files):
    with open(dir+"/"+file, "r") as text:
        text = text.read().lower()

        #remove punctation and \n
        text = text.translate(str.maketrans('', '', punctuation+"«»©"))
        text = text.replace("\n", " ")

        #split in words
        words = text.split(" ")
        
        words = [x for x in words if x != '']

        for i in range(len(words)-N+1):
            ngram = []
            for j in range(N):
                ngram.append(words[i+j])
            
            DB.addNgram(ngram)

print("finished generating model")