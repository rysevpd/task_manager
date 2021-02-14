import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from database import DB


class AdminPanel(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.init_main()
        self.db = db

    def init_main(self):
        menubar = Menu(master)
        master.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        search_menu = Menu(menubar, tearoff=0)
        print_menu = Menu(menubar, tearoff=0)

        search_menu.add_command(label="Поиск по задаче", command=self.search_tasks)
        search_menu.add_command(label="Поиск по категории", command=self.search_category)
        search_menu.add_command(label="Поиск по ответсвенному", command=self.search_user)

        file_menu.add_command(label="Добавить категорию", command=self.add_category)
        file_menu.add_command(label="Добавить пользователя", command=self.add_user)
        file_menu.add_command(label="Добавить задачу", command=self.add_task)
        file_menu.add_command(label="Показать пользователей", command=self.list_users)

        print_menu.add_command(label="Печать задач", command=self.print_data)
        print_menu.add_command(label="Печать пользователей", command=self.print_users)

        menubar.add_cascade(label="Файл", menu=file_menu)
        menubar.add_cascade(label="Поиск", menu=search_menu)
        menubar.add_command(label="Помощь", command=self.open_help_dialog)
        menubar.add_cascade(label="Печать", menu=print_menu)
        # menubar.add_command(label="Обновить", command=self.view_records)

        frame_1 = LabelFrame(self.master, text="Управление", bg="#3d394d", fg="#ffb26b",
                             font="Times 15")
        frame_1.pack(side=RIGHT, padx=2, fill=Y)

        update_data = tk.Button(frame_1,
                                text='Редактировать',
                                bg="#403c4a",
                                # bd=2,
                                font='Times 15'  # command=self.open_update_dialog
                                )
        update_data.pack(side=TOP, padx=5, pady=5)

        del_data = tk.Button(frame_1,
                             text='     Удалить     ',
                             bg="#403c4a",
                             bd=2,
                             font='Times 15')
        del_data.pack(side=TOP, padx=5, pady=5)

        del_data = tk.Button(frame_1,
                             text='     Обновить   ',
                             bg="#403c4a",
                             bd=2,
                             font='Times 15')
        del_data.pack(side=TOP, padx=5, pady=5)

        programmer = tk.Button(frame_1,
                               text='О разработчике',
                               bg="#403c4a",
                               bd=2,
                               font='Times 15')
        programmer.pack(side=TOP, padx=5, pady=5)

        poetry = "Не задерживайтесь\n" \
                 "в прошлом, не мечтайте\n" \
                 "о будущем, сосредоточьте\n " \
                 "разум на настоящем.\n" \
                 "© Будда"
        label2 = tk.Label(frame_1, text=poetry,
                          bg="#3d394d", fg="#ffb26b")
        label2.pack(side=TOP)

        exit_program = tk.Button(frame_1,
                                 text='      Выход      ',
                                 bg="#ef4f4f",
                                 bd=2,
                                 font='Times 15', command=master.quit)
        exit_program.pack(side=BOTTOM, padx=5, pady=5)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11), foreground="#008891")  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'),
                        bg="#008891")  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders)

        """Виджет tree - наша таблица"""
        frame_2 = LabelFrame(self.master,
                             text="Задачи",
                             bg="#3d394d",
                             fg="#ffb26b",
                             font="Times 15")
        frame_2.pack(side=LEFT, fill=BOTH)
        self.tree = ttk.Treeview(frame_2,
                                 style="mystyle.Treeview",
                                 columns=('ID', 'task', 'category', 'status', 'responsible', 'date_start', 'date_end'),
                                 height=20,
                                 show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('task', anchor=tk.CENTER)
        self.tree.column('category', anchor=tk.CENTER)
        self.tree.column('status', anchor=tk.CENTER)
        self.tree.column('responsible', anchor=tk.CENTER)
        self.tree.column('date_start', anchor=tk.CENTER)
        self.tree.column('date_end', anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('task', text='Задча')
        self.tree.heading('category', text='Категория')
        self.tree.heading('status', text='Статус')
        self.tree.heading('responsible', text='Ответственный')
        self.tree.heading('date_start', text='Начало')
        self.tree.heading('date_end', text='Срок')
        self.tree.pack(side=LEFT, pady=3, padx=3, fill=BOTH)

    def record_user(self, user, login, pas, role, post, number, address):
        self.db.insert_user(user, login, pas, role, post, number, address)

    def record_category(self, category):
        self.db.insert_category(category)

    def records(self, task, category, status, responsible, date_start, date_end):
        self.db.insert_data(task, category, status, responsible, date_start, date_end)
        self.view_records()

    def update_record(self, task, category, status, responsible, date_start, date_end):
        self.db.c.execute('''UPDATE tasks SET task=?, category=?, status=?, responsible=?, date_start=?, date_end=? 
                             WHERE ID=?''',
                          (task, category, status, responsible, date_start, date_end,
                           self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM tasks''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM tasks WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, category):
        category = ('%' + category + '%',)
        self.db.c.execute('''SELECT * FROM tasks WHERE category LIKE ?''', category)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def search_records_t(self, task):
        task = ('%' + task + '%',)
        self.db.c.execute('''SELECT * FROM tasks WHERE task LIKE ?''', task)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def search_records_g(self, responsible):
        responsible = ('%' + responsible + '%',)
        self.db.c.execute('''SELECT * FROM tasks WHERE responsible LIKE ?''', responsible)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    @staticmethod
    def add_task():
        Task()

    @staticmethod
    def add_user():
        AddUser()

    @staticmethod
    def add_category():
        Category()

    @staticmethod
    def open_update_dialog():
        Update()

    @staticmethod
    def search_category():
        SearchCategory()

    @staticmethod
    def search_tasks():
        Search_Tasks()

    @staticmethod
    def search_user():
        SearchUser()

    @staticmethod
    def open_help_dialog():
        Help()

    @staticmethod
    def print_data():
        Print()

    @staticmethod
    def list_users():
        ListUsers()

    @staticmethod
    def print_users():
        PrintUsers()


class ListUsers(tk.Toplevel):
    def __init__(self):
        super().__init__(master)
        self.init_list_users()
        self.view = app
        self.db = db
        self.view_users()

    def init_list_users(self):
        self.title('Сотрудники')
        self.geometry("950x450+400+100")
        self.resizable(False, False)

        frame_1 = Frame(self, bg="#3d394d")
        frame_1.pack(side=BOTTOM, padx=2, fill=X)

        self.user_del = tk.Button(frame_1,
                                  bg='#00587a',
                                  fg='#ffffff',
                                  text=' УДАЛИТЬ ',
                                  compound=tk.TOP,
                                  font='Times 13',
                                  command=self.delete_users,
                                  width=20)
        self.user_del.pack(side=LEFT, padx=5, pady=5)

        btn_cancel = tk.Button(frame_1,
                               bg='#00587a',
                               fg='#ffffff',
                               text=' ЗАКРЫТЬ ',
                               compound=tk.TOP,
                               font='Times 13',
                               command=self.destroy,
                               width=20)
        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

        frame_2 = LabelFrame(self,
                             text="Сотрудники",
                             bg="#3d394d",
                             fg="#ffb26b",
                             font="Times 15")
        frame_2.pack(side=TOP, fill=BOTH, padx=5, pady=5)

        """Виджет tree - наша таблица"""

        self.tree = ttk.Treeview(frame_2, columns=('name', 'login', 'pas', 'role', 'post', 'number', 'address'),
                                 height=15, show='headings')

        self.tree.column('name', width=180, anchor=tk.CENTER)
        self.tree.column('login', width=100, anchor=tk.CENTER)
        self.tree.column('pas', width=100, anchor=tk.CENTER)
        self.tree.column('role', width=70, anchor=tk.CENTER)
        self.tree.column('post', width=180, anchor=tk.CENTER)
        self.tree.column('number', width=130, anchor=tk.CENTER)
        self.tree.column('address', width=180, anchor=tk.CENTER)

        self.tree.heading('name', text='ФИО')
        self.tree.heading('login', text='Логин')
        self.tree.heading('pas', text='Пароль')
        self.tree.heading('role', text='Роль')
        self.tree.heading('post', text='Должность')
        self.tree.heading('number', text='Номер т.')
        self.tree.heading('address', text='Адрес')

        self.tree.pack()


    def view_users(self):
        self.db.c.execute('''SELECT * FROM users''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_users(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM users WHERE name=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_users()


class AddUser(tk.Toplevel):
    """Окно добавления нового пользователя"""

    def __init__(self):
        super().__init__(master)
        self.init_user()
        self.view = app

    def init_user(self):
        self.title('Добавить сотрудника')
        self.geometry('400x400+400+100')
        self.resizable(False, False)

        frame_1 = Frame(self, bg="#e7e7de")
        frame_1.pack(fill=X)
        label_user = tk.Label(frame_1,
                                  text='ФИО сотрудника:',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_user.pack(side=LEFT, padx=5, pady=5)

        entry_user = Entry(frame_1, justify="right")
        entry_user.pack(fill=X, padx=5, expand=True)

        frame_2 = Frame(self, bg="#e7e7de")
        frame_2.pack(fill=X)
        label_login = tk.Label(frame_2,
                                  text='Логин:                   ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_login.pack(side=LEFT, padx=5, pady=5)

        # entry_login = Entry(frame_2, justify="right")
        entry_login = Entry(frame_2, justify="right")
        entry_login.pack(fill=X, padx=5, expand=True)

        frame_3 = Frame(self, bg="#e7e7de")
        frame_3.pack(fill=X)
        label_pas = tk.Label(frame_3,
                                  text='Пароль:                 ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_pas.pack(side=LEFT, padx=5, pady=5)

        entry_pas = Entry(frame_3, justify="right")
        entry_pas.pack(fill=X, padx=5, expand=True)

        frame_4 = Frame(self, bg="#e7e7de")
        frame_4.pack(fill=X)
        label_role = tk.Label(frame_4,
                                  text='Роль:                     ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_role.pack(side=LEFT, padx=5, pady=5)

        entry_role = ttk.Combobox(frame_4, values=[u'admin', u'user'])
        entry_role.current(0)
        entry_role.pack(fill=X, padx=5, expand=True)

        frame_5 = Frame(self, bg="#e7e7de")
        frame_5.pack(fill=X)
        label_post = tk.Label(frame_5,
                                  text='Должность:          ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_post.pack(side=LEFT, padx=5, pady=5)

        entry_post = Entry(frame_5, justify="right")
        entry_post.pack(fill=X, padx=5, expand=True)

        frame_6 = Frame(self, bg="#e7e7de")
        frame_6.pack(fill=X)
        label_number = tk.Label(frame_6,
                                  text='Номер телефона: ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_number.pack(side=LEFT, padx=5, pady=5)

        entry_number = Entry(frame_6, justify="right")
        entry_number.pack(fill=X, padx=5, expand=True)

        frame_7 = Frame(self, bg="#e7e7de")
        frame_7.pack(fill=X)

        label_address = tk.Label(frame_7,
                                  text='Адрес:                   ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_address.pack(side=LEFT, padx=5, pady=5)

        entry_address = Entry(frame_7, justify="right")
        entry_address.pack(fill=X, padx=5, expand=True)

        frame_8 = Frame(self, bg="#e7e7de")
        frame_8.pack(fill=X)

        btn_cancel = tk.Button(frame_8,
                               bg='#00587a',
                               fg='#ffffff',
                               text=' ЗАКРЫТЬ ',
                               compound=tk.TOP,
                               font='Times 13',
                               command=self.destroy,
                               width=20)
        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

        self.btn_ok = tk.Button(frame_8,
                                bg='#00587a',
                                fg='#ffffff',
                                text='ДОБАВИТЬ',
                                compound=tk.TOP,
                                font='Times 13',
                                width=20)

        self.btn_ok.pack(side=LEFT, padx=5, pady=5)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(entry_user.get(),
                                                                       entry_login.get(),
                                                                       entry_pas.get(),
                                                                       entry_role.get(),
                                                                       entry_post.get(),
                                                                       entry_number.get(),
                                                                       entry_address.get()))

        self.grab_set()
        self.focus_set()

        frame_9 = Frame(self, bg="#e7e7de")
        frame_9.pack(fill=X)

        poetry = "Умеющий управлять другими силен,\n" \
                 "но умеющий владеть собой ещё сильнее.\n" \
                 "© Лао-Цзы"
        label2 = tk.Label(frame_9, text=poetry,
                          bg="#e7e7de")
        label2.pack(padx=2, pady=7)

class Category(tk.Toplevel):
    """Окно добавления категории"""

    def __init__(self):
        super().__init__(master)
        self.init_category()
        self.view = app

    def init_category(self):
        self.title('Добавить категорию')
        self.geometry('400x120+400+100')
        self.resizable(False, False)
        frame_1 = Frame(self, bg="#e7e7de")
        frame_1.pack(fill=X)

        label_category = tk.Label(frame_1,
                                  text='Название категории:',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_category.pack(side=LEFT, padx=5, pady=5)

        entry_login = Entry(frame_1, justify="right")
        entry_login.pack(fill=X, padx=5, expand=True)

        frame_2 = Frame(self, bg="#e7e7de")
        frame_2.pack(fill=X)

        btn_cancel = tk.Button(frame_2,
                               bg='#00587a',
                               fg='#ffffff',
                               text=' ЗАКРЫТЬ ',
                               compound=tk.TOP,
                               font='Times 13',
                               command=self.destroy,
                               width=20)
        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

        btn_ok = tk.Button(frame_2,
                           bg='#00587a',
                           fg='#ffffff',
                           text=' ВХОД ',
                           compound=tk.TOP,
                           font='Times 13',
                           width=20)
        btn_ok.pack(side=LEFT, padx=5, pady=5)
        btn_ok.bind('<Button-1>', lambda event: self.view.record_category(self.entry_category.get()))

        self.grab_set()
        self.focus_set()

        frame_3 = Frame(self, bg="#e7e7de")
        frame_3.pack(fill=X)

        poetry = "Плох тот план, который нельзя изменить\n" \
                 "© Публилий Сир"
        label = tk.Label(frame_3, text=poetry, bg="#e7e7de")
        label.pack(side=BOTTOM, padx=2, pady=1)


class Task(tk.Toplevel):
    """Окно добавления задачи"""

    def __init__(self):
        super().__init__(master)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить задачу')
        self.geometry('400x420+400+100')
        self.resizable(False, False)

        frame_1 = Frame(self, bg="#e7e7de")
        frame_1.pack(fill=X)
        label_task = tk.Label(frame_1,
                                  text='Задача:               ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_task.pack(side=LEFT, padx=5, pady=5)

        entry_task = Entry(frame_1, justify="right")
        entry_task.pack(fill=X, padx=5, expand=True)

        frame_2 = Frame(self, bg="#e7e7de")
        frame_2.pack(fill=X)
        label_category = tk.Label(frame_2,
                                  text='Категория:         ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_category.pack(side=LEFT, padx=5, pady=5)

        # entry_login = Entry(frame_2, justify="right")
        entry_category = ttk.Combobox(frame_2, values=[u'TODO', u'in progress', u'suspended', u'DONE'])
        entry_category.pack(fill=X, padx=5, expand=True)

        frame_3 = Frame(self, bg="#e7e7de")
        frame_3.pack(fill=X)
        label_status = tk.Label(frame_3,
                                  text='Статус:               ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_status.pack(side=LEFT, padx=5, pady=5)

        entry_status = Entry(frame_3, justify="right")
        entry_status.pack(fill=X, padx=5, expand=True)

        frame_4 = Frame(self, bg="#e7e7de")
        frame_4.pack(fill=X)
        label_responsible = tk.Label(frame_4,
                                  text='Ответственный:',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_responsible.pack(side=LEFT, padx=5, pady=5)

        entry_responsible = Entry(frame_4, justify="right")
        entry_responsible.pack(fill=X, padx=5, expand=True)

        frame_5 = Frame(self, bg="#e7e7de")
        frame_5.pack(fill=X)
        label_date_start = tk.Label(frame_5,
                                  text='Старт задачи:    ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_date_start.pack(side=LEFT, padx=5, pady=5)

        entry_date_start = Entry(frame_5, justify="right")
        entry_date_start.pack(fill=X, padx=5, expand=True)

        frame_6 = Frame(self, bg="#e7e7de")
        frame_6.pack(fill=X)
        label_date_end = tk.Label(frame_6,
                                  text='Срок до:             ',
                                  bg="#e7e7de",
                                  font='Times 15')
        label_date_end.pack(side=LEFT, padx=5, pady=5)

        entry_date_end = Entry(frame_6, justify="right")
        entry_date_end.pack(fill=X, padx=5, expand=True)

        frame_7 = Frame(self, bg="#e7e7de")
        frame_7.pack(fill=X)


        btn_cancel = tk.Button(frame_7,
                               bg='#00587a',
                               fg='#ffffff',
                               text=' ЗАКРЫТЬ ',
                               compound=tk.TOP,
                               font='Times 13',
                               command=self.destroy,
                               width=20)
        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

        self.btn_ok = tk.Button(frame_7,
                                bg='#00587a',
                                fg='#ffffff',
                                text='ДОБАВИТЬ',
                                compound=tk.TOP,
                                font='Times 13',
                                width=20)

        self.btn_ok.pack(side=LEFT, padx=5, pady=5)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(entry_task.get(),
                                                                       entry_category.get(),
                                                                       entry_status.get(),
                                                                       entry_responsible.get(),
                                                                       entry_date_start.get(),
                                                                       entry_date_end.get()))

        self.grab_set()
        self.focus_set()

        frame_8 = Frame(self, bg="#e7e7de")
        frame_8.pack(fill=X)

        poetry = "Чтобы выполнить большой и важный труд,\n " \
                 "необходимы две вещи: ясный план \n" \
                 "и ограниченное время\n" \
                 "© Хаббард Элберт"
        label2 = tk.Label(frame_8,
                          text=poetry,
                          bg="#3d394d",
                          fg="#ffb26b")
        label2.pack(side=TOP)


class Update(Task):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать данные')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=180, y=270)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_task.get(),
                                                                          self.entry_category.get(),
                                                                          self.entry_status.get(),
                                                                          self.entry_responsible.get(),
                                                                          self.entry_date_start.get(),
                                                                          self.entry_date_end.get()))

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM tasks WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_task.insert(0, row[1])
        self.entry_category.insert(0, row[2])
        self.entry_responsible.insert(0, row[4])
        self.entry_date_start.insert(0, row[5])
        self.entry_date_end.insert(0, row[6])
        self.entry_status.current(0, row[3])


class SearchCategory(tk.Toplevel):
    """Окно поиска по категории"""

    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск по категории')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class Search_Tasks(tk.Toplevel):
    """Окно поиска по задаче"""

    def __init__(self):
        super().__init__()
        self.init_search_t()
        self.view = app

    def init_search_t(self):
        self.title('Поиск по задаче')
        self.geometry('300x100+400+300')

        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records_t(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class SearchUser(tk.Toplevel):
    """Поиск по ФИО ответственного"""

    def __init__(self):
        super().__init__()
        self.init_search_g()
        self.view = app

    def init_search_g(self):
        self.title('Поиск по ФИО ответсвенного')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records_g(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class Help(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.window_help()
        self.view = app

    def window_help(self):
        self.title('Помощь')
        self.geometry('750x550+300+200')
        self.resizable(False, False)
        self.text = tk.Text(self)
        self.text.insert(1.0, 'Добро пожаловать в приложение - Менеджер задач. Пройдемся по функционалу\n1. Файл\n'
                              '1.1. Добавить категорию - добавить категорию в журнал.\n1.2. Добавить пользователя - '
                              'добавить пользователя в '
                              ' журнал.\n1.3. Добавить задачу - добавить задачу в журнал. ВАЖНО: Чтобы добавить задачу'
                              'в журнал, убедитесь, что его категория и ответственный уже добавлены в систему, '
                              'иначе задача не будет '
                              'добавлен в систему.\n1.4 - Посмотреть пользователей - откроет окно просмотра '
                              'информации о всех пользователях \n '
                              '2. Поиск\n2.1 Поиск по категории - выведет все задачи из этой категории'
                              '.\n2.2. Поиск по ответственному - выведет все, что есть принадлежит данному '
                              'человеку.\n2.3. '
                              'Поиск по названию задачи - будет искать совпадения в графе задачи.\n3. Печать - в '
                              'директории, в которой ра '
                              'сположено приложение, будет создан текстовый документ с той информацией, выгрузку '
                              'которой вы выбрали.\n4. Обнови '
                              'ть - обновить информацию в таблице.\n5. Редактировать - если хотите изменить '
                              'информацию в задаче '
                              ' в таблице, просто выделите строку с нужной задачей и кликнете по клавише ИЗМЕНИТЬ.\n6. '
                              'Удалить - если вам надо удалить задачу, то выделите ее в таблице '
                              'и нажмите УДАЛИТЬ. Так же можно выделить сразу несколько строк.\nЕсли у вас есть пожелан'
                              'е по работе приложения, или вы заметили ошибку, напишите мне '
                              'https://github.com/rysevpd/task-manager/issues/new')
        self.text.pack()


class Print:
    def __init__(self):
        self.conn = sqlite3.connect('manager.db')
        self.c = self.conn.cursor()

        z = self.c.execute('''SELECT * FROM tasks''', )

        y = str(z.fetchall())
        f = open('выгрузка_задачи.txt', 'w+')
        f.write(
            ' id ' + "\t" + 'Задача      ' + "\t" + '     Категория' + "\t" + "   Статус" + "\t" + 'Ответственный' + "\t" + 'начало' + "\t" + '      срок' + "\n")
        f.write(y + '\n')
        f.close()

        with open('выгрузка_задачи.txt', 'r') as file:
            file_data = file.read()

        file_data = file_data.replace('),', '. \n')
        file_data = file_data.replace('[', ' ')
        file_data = file_data.replace("'", ' ')
        file_data = file_data.replace(',', ' --- ')
        file_data = file_data.replace('(', '')
        file_data = file_data.replace(')', '')
        file_data = file_data.replace(']', '')

        with open('выгрузка_задачи.txt', 'w+') as file:
            file.write(file_data)


class PrintUsers():
    def __init__(self):
        self.conn = sqlite3.connect('manager.db')
        self.c = self.conn.cursor()

        z = self.c.execute('''SELECT * FROM users''', )

        y = str(z.fetchall())
        f = open('выгрузка_пользователей.txt', 'w+')
        f.write(
            '   ФИО   ' + "\t" + '      логин   ' + "\t" + '   пароль  ' + "\t" + "  роль  " + "\t" + '   должность  ' + "\t" + '  номер т.  ' + "\t" + '   адрес проживания' + "\n")
        f.write(y + '\n')
        f.close()

        with open('выгрузка_пользователей.txt', 'r') as file:
            file_data = file.read()

        file_data = file_data.replace('),', '. \n')
        file_data = file_data.replace('[', ' ')
        file_data = file_data.replace("'", ' ')
        file_data = file_data.replace(',', ' --- ')
        file_data = file_data.replace('(', '')
        file_data = file_data.replace(')', '')
        file_data = file_data.replace(']', '')

        with open('выгрузка_пользователей.txt', 'w+') as file:
            file.write(file_data)


if __name__ == "__main__":
    """Запуск приложения"""
    db = DB()
    master = Tk()
    master.geometry("1400x650+100+100")
    master.title("Задачи")
    master.config(bg="#3d394d")
    app = AdminPanel(master)
    app.pack()
    master.mainloop()
