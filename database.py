import sqlite3

class Database:
    def __init__(self, path, n, commit_interval=1000):
        self.n = n
        self.filepath = path
        self.table_name = f"ngrams_{self.n}"
        self.table_columns = ", ".join([f"word{i} TEXT" for i in range(1, n + 1)])
        self.create_table_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} (count INTEGER, {self.table_columns})"
        
        self.connect_to_database()

        self.commit_counter = 0
        self.commit_interval = commit_interval

    def connect_to_database(self):
        self.connection = sqlite3.connect(self.filepath)
        self.cursor = self.connection.cursor()

        self.cursor.execute(self.create_table_query)
        self.connection.commit()

    def addNgram(self, words):
        value_test_string = " AND ".join([f'word{i+1}=?' for i in range(len(words))])

        existing_row_count = self.cursor.execute(
            f"SELECT COUNT(*) FROM {self.table_name} WHERE {value_test_string}",
            words
        ).fetchone()[0]

        with self.connection:
            if existing_row_count > 0:
                update_query = (
                    f"UPDATE {self.table_name} SET count = count + 1 WHERE {value_test_string}"
                )
                self.cursor.execute(update_query, words)
            else:
                value_string = ", ".join([f'word{i+1}' for i in range(len(words))])
                placeholders = ", ".join(["?" for _ in range(len(words) + 1)])
                insert_query = (
                    f"INSERT INTO {self.table_name} ({value_string}, count) VALUES ({placeholders})"
                )
                values = words + [1]
                self.cursor.execute(insert_query, values)

        self.commit_counter += 1
        if self.commit_counter >= self.commit_interval:
            self.commit_counter = 0
            self.connection.commit()

    def query(self, words):
        value_test_string = " AND ".join([f'word{i+1}=?' for i in range(len(words))])

        return self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE {value_test_string}", words)
