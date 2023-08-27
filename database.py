import sqlite3

class Database:
    def __init__(self, path, n, commit_interval=5000):
        self.n = n
        self.filepath = path
        self.words_table_name = "words"
        self.create_words_table_query = f"CREATE TABLE IF NOT EXISTS {self.words_table_name} (word_id INTEGER PRIMARY KEY, word TEXT)"
        
        self.tablenames = {}

        self.connect_to_database()
        self.create_all_tables()

        self.commit_counter = 0
        self.commit_interval = commit_interval

    def connect_to_database(self):
        self.connection = sqlite3.connect(self.filepath)
        self.cursor = self.connection.cursor()

    def create_all_tables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "words" ( "id" INTEGER, "string" TEXT UNIQUE, PRIMARY KEY("id" AUTOINCREMENT));')

        for char in "abcdefghijklmnopqrstuvwxyz":
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS ngrams{self.n}{char} (count INT,{' INT,'.join([f'word{i} INT' for i in range(1, self.n+1)]) + ' INT'},PRIMARY KEY ({', '.join([f'word{i}' for i in range(1, self.n+1)])}));")
            self.tablenames[char] = f"ngrams{self.n}{char}"

    def addNgram(self, words: list[str]):
        try:
            tableName = self.tablenames.get(words[0][0])

            if (tableName == None): return
        except KeyError:
            return

        
        placeholders = ','.join(['?'] * (len(words) + 1))
        columns = ', '.join(['count'] + [f'word{i}' for i in range(1, len(words) + 1)])
        
        insert_query = f"INSERT INTO {tableName} ({columns}) VALUES ({placeholders}) ON CONFLICT({', '.join([f'word{i}' for i in range(1, len(words) + 1)])}) DO UPDATE SET count = count + 1;"
        
        values = [(1,) + tuple(map(self.getWordId, words))]

        #huge performace boost!
        self.cursor.executemany(insert_query, values)

        self.commit_counter += 1

        if self.commit_counter >= self.commit_interval:
            self.commit()

    def getWordId(self, word):
        self.cursor.execute('INSERT OR IGNORE INTO words (string) VALUES (?)', (word,))
        self.cursor.execute('SELECT id FROM words WHERE string = ?', (word,))
        return self.cursor.fetchone()[0]
    
    def getWordById(self, id):
        self.cursor.execute('SELECT string FROM words WHERE id = ?', (id,))
        return self.cursor.fetchone()[0]

    def commit(self):
        self.connection.commit()
        self.commit_counter = 0

    def getNextWord(self, lastnwords):
        try:
            tableName = self.tablenames.get(lastnwords[0][0])

            if tableName is None:
                return "ERROR!"
        except KeyError:
            return "ERROR!"

        testString = ' AND '.join([f'word{i} = ? ' for i in range(1, self.n-1 + 1)])

        self.cursor.execute(f"SELECT word{self.n} FROM {tableName} WHERE {testString} ORDER BY count DESC LIMIT 1", list(map(self.getWordId, lastnwords)))
        return self.getWordById(self.cursor.fetchone()[0]);

    def query(self, words, n):
        wordorder = words.copy()

        for _ in range(n):
            print(wordorder[-(self.n-1):])
            try:
                wordorder.append(self.getNextWord(wordorder[-(self.n-1):]))
            except:
                return " ".join(wordorder)
            
        return " ".join(wordorder)

