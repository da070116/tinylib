import tkinter as tk
from tkinter import ttk


def place_with_label(x, y, parent, entry, title, value):
    label = tk.Label(parent, text=title)
    label.place(x=x, y=y)
    entry_x = 8 * 10 + 15
    entry.place(x=entry_x, y=y)
    entry.insert(0, value)


class ManageBookWindow:
    """docstring for Window"""

    def __init__(self, parent, db_connection, width, height, title, resizable, values):

        # Database init
        self.db_manager = db_connection
        # Values (if any)
        if not values:
            values = ['', '', '', '']
        self.id_value = values[0]
        self.author_value = values[1]
        self.title_value = values[2]
        self.location_value = values[3]
        # main window setup
        self.root = tk.Toplevel(parent)
        self.root.takefocus = True
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+250+250")
        self.root.resizable(resizable[0], resizable[1])
        # input fields
        self.entry_author = ttk.Entry(self.root)
        place_with_label(x=10, y=50, parent=self.root, entry=self.entry_author, title='Автор',
                         value=self.author_value)
        self.entry_title = ttk.Entry(self.root)
        place_with_label(x=10, y=80, parent=self.root, entry=self.entry_title, title='Название',
                         value=self.title_value)
        self.entry_location = ttk.Entry(self.root)
        place_with_label(x=10, y=110, parent=self.root, entry=self.entry_location, title='Место',
                         value=self.location_value)
        # buttons
        self.btn_add_book = ttk.Button(self.root, text='OK', command=self.add_or_update)

        self.btn_add_book.place(x=80, y=140)
        self.btn_clear = ttk.Button(self.root, text='Clear', command=self.clear_values)
        self.btn_clear.place(x=180, y=140)
        # display on top (use as modal)
        self.root.grab_set()
        self.root.focus_set()
        self.root.transient(parent)
        self.root.wait_window()

    # def add_new(self):
    # 	author = self.entry_author.get()
    # 	title = self.entry_title.get()
    # 	location = self.entry_location.get()
    # 	self.db_manager.insert_data(id='', author=author, title=title, location=location)
    # 	print('Values added')
    # 	self.clear_values()

    def add_or_update(self):
        author = self.entry_author.get()
        title = self.entry_title.get()
        location = self.entry_location.get()
        print(f'{author=}, {title=},  {location=}')
        self.db_manager.insert_data(book_uid=self.id_value, author=author, title=title, location=location)
        if self.id_value != '':
            print('Values updated')
        else:
            print('Values added')
        self.clear_values()

    def clear_values(self):
        self.entry_author.delete(0, tk.END)
        self.entry_title.delete(0, tk.END)
        self.entry_location.delete(0, tk.END)
