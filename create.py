import database
from string import punctuation
from tqdm import tqdm

DBPATH   = "2gram.db"
N        = 2

DB = database.Database(DBPATH, N)

import os

dir = "texts"

files = os.listdir(dir)

toremove = [
    "<b>",
    "</b>",
    "<pre>",
    "</pre>",
    "<html>",
    "</html>",
    "<title>",
    "</title>",
    '<body bgcolor="#ffffff">',
    "<body>",
    "</body>",
    "<script>",
    "</script>",
    "if (window!= top)",
    "top.location.href=location.href",
    "// -->",
    " b "
]

print(f"{str(len(files))} files to process")
for file in tqdm(files):
    with open(dir+"/"+file, "r") as text:
        text = text.read().lower()

        #remove punctation and \n
        text = text.translate(str.maketrans('', '', punctuation+"«»©"))
        text = text.replace("\n", " ")
        for substr in toremove:
            text = text.replace(substr, " ")

        #split in words
        words = text.split(" ")
        
        words = [x for x in words if x != '']

        for i in range(len(words)-N+1):
            ngram = []
            for j in range(N):
                ngram.append(words[i+j])
            
            DB.addNgram(ngram)

print("finished generating model")
