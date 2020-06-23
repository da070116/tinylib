import tkinter as tk
from tkinter import ttk

from tinylib_pkg.dbmanager import DbManager
from tinylib_pkg.managebookwindow import ManageBookWindow


class Window:
    """docstring for Window"""

    def __init__(self, width, height, title="Main Window", resizable=None, icon=None):

        # Database init
        if resizable is None:
            resizable = [False, False]
        self.db_manager = DbManager()

        # main window setup
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+200+200")
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbitmap(icon)

        # Toolbar menu
        self.toolbar = tk.Frame(bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.btn_add = tk.Button(self.toolbar, text='Add book', command=self.add_new, compound=tk.TOP)
        self.btn_add.pack(side=tk.LEFT)
        self.btn_edit = tk.Button(self.toolbar, text='Edit book', command=self.edit, compound=tk.TOP)
        self.btn_edit.pack(side=tk.LEFT)
        self.btn_delete = tk.Button(self.toolbar, text='Delete', command=self.delete_records, compound=tk.TOP)
        self.btn_delete.pack(side=tk.LEFT)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Author', 'Title', 'Location'), height=20, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('Author', width=100, anchor=tk.CENTER)
        self.tree.column('Title', width=150, anchor=tk.CENTER)
        self.tree.column('Location', width=120, anchor=tk.CENTER)

        self.tree.heading('ID', text='№', command=self.order_by_id)
        self.tree.heading('Author', text='Автор', command=self.order_by_author)
        self.tree.heading('Title', text='Название', command=self.order_by_title)
        self.tree.heading('Location', text='Место', command=self.order_by_location)

        self.order_by_id()
        self.tree.pack()

    def order_by_id(self):
        self.list_records(order_by='id')

    def order_by_author(self):
        self.list_records(order_by='author')

    def order_by_title(self):
        self.list_records(order_by='title')

    def order_by_location(self):
        self.list_records(order_by='location')

    def run(self):
        self.root.mainloop()

    def add_new(self):

        ManageBookWindow(self.root, self.db_manager, 300, 200, 'Add new book', [False, False], values=None)
        self.order_by_id()

    def edit(self):
        sel = self.tree.selection()
        if len(sel) == 1:
            values = [self.tree.set(sel, '#1'),
                      self.tree.set(sel, '#2'),
                      self.tree.set(sel, '#3'),
                      self.tree.set(sel, '#4')]
            ManageBookWindow(self.root, self.db_manager, 300, 200, 'Edit book', [False, False], values=values)
            self.order_by_id()

    def list_records(self, order_by):
        result = self.db_manager.list_all(order_by=order_by)
        if result:
            [self.tree.insert('', 'end', values=r) for r in result]

    def delete_records(self):
        if len(self.tree.selection()) > 0:
            for selected_item in self.tree.selection():
                delete_id = self.tree.set(selected_item, '#1')
                self.db_manager.delete_record(book_uid=delete_id)
                self.order_by_id()
