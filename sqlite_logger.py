import sqlite3
import time


class SQLiteLogger:
    def __init__(self):
        self.dbfile = "test.db"
        create_table = True

        try:
            with open(self.dbfile):
                create_table = False
        except IOError:
            pass

        self.connection = sqlite3.connect(self.dbfile)

        if create_table:
            cursor = self.connection.cursor()
            cursor.execute('''CREATE TABLE readings
                              (date real, device text, property text, value real)''')
            self.connection.commit()

    def log(self, device, property, value):
        now = time.time()
        values = (now, device, property, value)

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO readings VALUES(?,?,?,?)", values)
        self.connection.commit()


    def close(self):
        self.connection.close()
