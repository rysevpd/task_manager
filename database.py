import sqlite3


class DB:
    """Взаимодействие с дб."""
    def __init__(self):
        self.conn = sqlite3.connect('manager.db')
        self.c = self.conn.cursor()

        self.c.execute(
            '''PRAGMA foreign_keys=on''')
        self.conn.commit()

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS status(
            status text primary key)''')
        self.conn.commit()

        self.c.execute(
            '''INSERT OR IGNORE INTO status (status)
            VALUES ('TODO'), 
            ('in progress'),
            ('suspended'),
            ('DONE')''')
        self.conn.commit()

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS category(
            category text primary key)''')
        self.conn.commit()

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS users(
            name text primary key,
            login text,
            pas text,
            role text,
            post text,
            number text,
            address text)''')
        self.conn.commit()


        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS tasks(
            id integer primary key, 
            task text, 
            category text,
            status text,
            responsible text,
            date_start text,
            date_end text,
            FOREIGN KEY (category) REFERENCES category(category),
            FOREIGN KEY (status) REFERENCES status(status),
            FOREIGN KEY (responsible) REFERENCES users(name))''')
        self.conn.commit()

    def insert_user(self, user, login, pas, role, post, number, address):
        self.c.execute(
            '''INSERT INTO users(name, login, pas, role, post, number, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (user, login, pas, role, post, number, address,))
        self.conn.commit()

    def insert_category(self, category):
        self.c.execute(
            '''INSERT INTO category(category)
            VALUES (?)''',
            (category,))
        self.conn.commit()


    def insert_data(self, task, category, status, responsible, date_start, date_end):
        self.c.execute(
            '''INSERT INTO tasks(task, category, status, responsible, date_start, date_end)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (task, category, status, responsible, date_start, date_end))
        self.conn.commit()