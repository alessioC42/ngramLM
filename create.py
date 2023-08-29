import database
from string import punctuation
from tqdm import tqdm
from re import sub

DBPATH   = "6gram.db"
N        = 6

DB = database.Database(DBPATH, N)

import os

dir = "texts"

files = os.listdir(dir)

toremove = [
    "if (window!= top)",
    "top.location.href=location.href",
    " b "
]

print(f"{str(len(files))} files to process")
print(f"N = {N}")
for file in tqdm(files):
    with open(dir+"/"+file, "r") as text:
        text = text.read()

        text = sub(r'<.*?>', '', text)

        for substr in toremove:
            text = text.replace(substr, " ")

        text = text.lower()

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
