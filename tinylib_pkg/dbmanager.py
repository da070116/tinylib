import sqlite3


class DbManager(object):
    """

    """

    def __init__(self):
        self.connection = sqlite3.connect('library.db')
        self.c = self.connection.cursor()
        self.query_result = []
        # build table
        self.execute_query('''CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY,
                             author TEXT NOT NULL,
                             title TEXT NOT NULL, 
                             location TEXT NOT NULL)'''
                           )

    def insert_data(self, book_uid, author, title, location):
        if not book_uid:
            _q = f'INSERT INTO books(author, title, location) VALUES("{author}", "{title}", "{location}")'
        else:
            _q = f'UPDATE books SET author="{author}", title="{title}", location="{location}" WHERE id={book_uid} '
        print(f'{_q=}')

        if author.strip() != '' and title.strip() != '' and location.strip() != '':
            self.execute_query(_q)

    def list_all(self, order_by):
        return self.execute_query(f'SELECT * FROM books ORDER BY {order_by} ASC')

    def delete_record(self, book_uid):
        self.execute_query(f'DELETE FROM books WHERE id={book_uid}')

    def execute_query(self, query: str):
        try:
            self.c.execute(query)
            self.connection.commit()
            if query.startswith('SELECT'):
                return self.c.fetchall()

        except sqlite3.Error:
            print("Database error")
            raise
