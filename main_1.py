import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import *



class Main(tk.Frame):
    """Основное окно программы."""

    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        frame_1 = LabelFrame(self.master,
                             text="Управление",
                             bg="#48466d",
                             fg="#bad7df",
                             font="Times 15")
        frame_1.pack(side=RIGHT, padx=2, fill=Y)

        update_data = tk.Button(frame_1,
                                text='Редактировать',
                                bg="#3d84a8",
                                fg="#bad7df",
                                font='Times 15',
                                command=self.open_update_dialog)
        update_data.pack(side=TOP, padx=5, pady=5)

        del_data = tk.Button(frame_1,
                             text='     Обновить   ',
                             bg="#3d84a8",
                             fg="#bad7df",
                             font='Times 15',
                             command=self.view_records)
        del_data.pack(side=TOP, padx=5, pady=5)


        poetry = "Не задерживайтесь\n" \
                 "в прошлом, не мечтайте\n" \
                 "о будущем, сосредоточьте\n " \
                 "разум на настоящем.\n" \
                 "© Будда"
        label2 = tk.Label(frame_1,
                          text=poetry,
                          bg="#48466d",
                          fg="#bad7df")
        label2.pack(side=TOP)

        update_data = tk.Button(frame_1,
                                text='      Выход      ',
                                bg="#ef4f4f",
                                fg="#bad7df",
                                font='Times 15',
                                command=root.quit)
        update_data.pack(side=BOTTOM, padx=5, pady=5)

        self.main_menu = Menu()
        self.file_menu = Menu(tearoff=0)
        self.search_menu = Menu(tearoff=0)
        self.print_menu = Menu(tearoff=0)

        self.search_menu.add_command(label="Поиск по задаче", command=self.search_tasks)
        self.search_menu.add_command(label="Поиск по категории", command=self.search_category)

        self.main_menu.add_cascade(label="Поиск", menu=self.search_menu)
        self.main_menu.add_command(label="Помощь", command=self.open_help_dialog)

        root.config(menu=self.main_menu)

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#48466d",
                        fieldbackground="#48466d",
                        foreground="#48466d")

        frame_2 = LabelFrame(self.master,
                             text="Задачи",
                             bg="#48466d",
                             fg="#bad7df",
                             font="Times 15")
        frame_2.pack(side=LEFT, fill=BOTH)

        self.tree = ttk.Treeview(frame_2,
                                 columns=('ID', 'task', 'category', 'status', 'responsible', 'date_start', 'date_end'),
                                 height=15,
                                 show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('task', anchor=tk.CENTER)
        self.tree.column('category', anchor=tk.CENTER)
        self.tree.column('status', anchor=tk.CENTER)
        self.tree.column('responsible', anchor=tk.CENTER)
        self.tree.column('date_start', anchor=tk.CENTER)
        self.tree.column('date_end', anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('task', text='Задача')
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
                         WHERE ID=?''', (
            task, category, status, responsible, date_start, date_end, self.tree.set(self.tree.selection()[0], '#1')))
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
    def open_update_dialog():
        Update()

    @staticmethod
    def search_category():
        SearchCategory()

    @staticmethod
    def search_tasks():
        Search_Tasks()

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
        super().__init__(root)
        self.init_listusers()
        self.view = app
        self.db = db
        self.view_users()

    def init_listusers(self):
        self.title('Сотруники')
        self.geometry("950x450+300+100")
        self.resizable(False, False)
        self.config(bg="#48466d")

        frame_1 = LabelFrame(self,
                             text="Сотрудники",
                             bg="#48466d",
                             fg="#bad7df",
                             font="Times 15")
        frame_1.pack(side=TOP, fill=BOTH)

        self.tree = ttk.Treeview(frame_1,
                                 columns=('name', 'login', 'pas', 'role', 'post', 'number', 'address'),
                                 height=15,
                                 show='headings')

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
        self.tree.pack(side=TOP, fill=BOTH, padx=4, pady=4)

        frame_2 = Frame(self, bg="#48466d")
        frame_2.pack(side=TOP, fill=X)

        update_data = tk.Button(frame_2,
                                bg='#3d84a8',
                                fg='#bad7df',
                                text='Удалить сотрудника',
                                compound=tk.TOP,
                                font='Times 13',
                                command=self.delete_users)
        update_data.pack(side=LEFT, padx=5, pady=5)

        btn_cancel = tk.Button(frame_2,
                               bg='#3d84a8',
                               fg='#bad7df',
                               text='    Закрыть    ',
                               compound=tk.TOP,
                               font='Times 13',
                               command=self.destroy)
        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

    def view_users(self):
        self.db.c.execute('''SELECT * FROM users''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_users(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM users WHERE name=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_users()




class Task(tk.Toplevel):
    """Окно добавления задачи"""

    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить задачу')
        self.geometry('400x420+400+100')
        self.resizable(False, False)
        self.config(bg="#48466d")

        frame_1 = Frame(self, bg="#48466d")
        frame_1.pack(fill=X)

        label_task = tk.Label(frame_1,
                              text='Задача:               ',
                              bg="#48466d",
                              fg="#bad7df",
                              font='Times 15')
        label_task.pack(side=LEFT, padx=5, pady=5)

        frame_2 = Frame(self, bg="#48466d")
        frame_2.pack(fill=X)
        label_category = tk.Label(frame_2,
                                  text='Категория:         ',
                                  bg="#48466d",
                                  fg="#bad7df",
                                  font='Times 15')
        label_category.pack(side=LEFT, padx=5, pady=5)

        frame_3 = Frame(self, bg="#48466d")
        frame_3.pack(fill=X)

        label_status = tk.Label(frame_3,
                                text='Статус:               ',
                                bg="#48466d",
                                fg="#bad7df",
                                font='Times 15')
        label_status.pack(side=LEFT, padx=5, pady=5)

        frame_4 = Frame(self, bg="#48466d")
        frame_4.pack(fill=X)
        label_responsible = tk.Label(frame_4,
                                     text='Ответственный:',
                                     bg="#48466d",
                                     fg="#bad7df",
                                     font='Times 15')
        label_responsible.pack(side=LEFT, padx=5, pady=5)

        frame_5 = Frame(self, bg="#48466d")
        frame_5.pack(fill=X)
        label_date_start = tk.Label(frame_5,
                                    text='Старт задачи:    ',
                                    bg="#48466d",
                                    fg="#bad7df",
                                    font='Times 15')
        label_date_start.pack(side=LEFT, padx=5, pady=5)

        frame_6 = Frame(self, bg="#48466d")
        frame_6.pack(fill=X)
        label_date_end = tk.Label(frame_6,
                                  text='Срок до:             ',
                                  bg="#48466d",
                                  fg="#bad7df",
                                  font='Times 15')
        label_date_end.pack(side=LEFT, padx=5, pady=5)

        self.entry_task = ttk.Entry(frame_1, justify="right")
        self.entry_task.pack(fill=X, padx=5, expand=True)
        self.entry_category = ttk.Entry(frame_2, justify="right")
        self.entry_category.pack(fill=X, padx=5, expand=True)

        self.entry_status = ttk.Combobox(frame_3, values=[u'TODO', u'in progress', u'suspended', u'DONE'])
        self.entry_status.current(0)
        self.entry_status.pack(fill=X, padx=5, expand=True)

        self.entry_responsible = ttk.Entry(frame_4, justify="right")
        self.entry_responsible.pack(fill=X, padx=5, expand=True)

        self.entry_date_start = ttk.Entry(frame_5, justify="right")
        self.entry_date_start.pack(fill=X, padx=5, expand=True)

        self.entry_date_end = ttk.Entry(frame_6, justify="right")
        self.entry_date_end.pack(fill=X, padx=5, expand=True)

        frame_7 = Frame(self, bg="#48466d")
        frame_7.pack(fill=X)

        btn_cancel = tk.Button(frame_7,
                               bg='#3d84a8',
                               fg='#bad7df',
                               text=' ЗАКРЫТЬ ',
                               compound=tk.TOP,
                               font='Times 13',
                               command=self.destroy,
                               width=20)
        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

        self.btn_ok = tk.Button(frame_7,
                                bg='#3d84a8',
                                fg='#bad7df',
                                text='ДОБАВИТЬ',
                                compound=tk.TOP,
                                font='Times 13',
                                width=20)
        self.btn_ok.pack(side=LEFT, padx=5, pady=5)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_task.get(),
                                                                       self.entry_category.get(),
                                                                       self.entry_status.get(),
                                                                       self.entry_responsible.get(),
                                                                       self.entry_date_start.get(),
                                                                       self.entry_date_end.get()))

        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.grab_set()
        self.focus_set()


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
        self.geometry('420x150+400+100')
        self.resizable(False, False)
        self.config(bg="#48466d")

        frame_1 = Frame(self, bg="#48466d")
        frame_1.pack(fill=X)

        label_search = tk.Label(frame_1,
                                text='Поиск',
                                bg='#48466d',
                                fg='#bad7df',
                                font='Times 15')
        label_search.pack(side=LEFT, padx=5, pady=5)

        self.entry_search = Entry(frame_1, justify="right")
        self.entry_search.pack(fill=X, padx=5, expand=True)

        frame_2 = Frame(self, bg="#48466d")
        frame_2.pack(fill=X)

        btn_cancel = tk.Button(frame_2,
                               bg='#3d84a8',
                               fg='#bad7df',
                               text=' ЗАКРЫТЬ ',
                               compound=tk.TOP,
                               font='Times 13',
                               command=self.destroy,
                               width=20)
        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

        btn_search = tk.Button(frame_2,
                               bg='#3d84a8',
                               fg='#bad7df',
                               text=' ПОИСК ',
                               compound=tk.TOP,
                               font='Times 13',
                               width=20)
        btn_search.pack(side=LEFT, padx=5, pady=5)
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
        self.geometry('420x150+400+100')
        self.resizable(False, False)
        self.config(bg="#48466d")

        frame_1 = Frame(self, bg="#48466d")
        frame_1.pack(fill=X)

        label_search = tk.Label(frame_1,
                                text='Поиск',
                                bg="#48466d",
                                fg="#bad7df",
                                font='Times 15')
        label_search.pack(side=LEFT, padx=5, pady=5)

        self.entry_search = Entry(frame_1, justify="right")
        self.entry_search.pack(fill=X, padx=5, expand=True)

        frame_2 = Frame(self, bg="#48466d")
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

        btn_search = tk.Button(frame_2,
                               bg='#00587a',
                               fg='#ffffff',
                               text=' ПОИСК ',
                               compound=tk.TOP,
                               font='Times 13',
                               width=20)
        btn_search.pack(side=LEFT, padx=5, pady=5)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records_t(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')





class Help(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.window_help()
        self.view = app

    def window_help(self):
        self.title('Помощь')
        self.geometry('850x550+400+80')
        self.resizable(False, False)
        self.config(bg="#48466d")

        frame_1 = LabelFrame(self,
                             text="Сводка по функционалу",
                             bg="#48466d",
                             fg="#bad7df",
                             font="Times 15")
        frame_1.pack(side=TOP, fill=BOTH, padx=5, pady=5)

        poetry = 'Добро пожаловать в приложение - Менеджер задач.\n ' \
                 'Пройдемся по функционалу. \n ' \
                 '1. Файл.                                                                                          ' \
                 '                                                             \n' \
                 '1.1. Добавить категорию - добавить категорию в журнал.                                             ' \
                 '                     \n' \
                 '1.2. Добавить пользователя - добавить пользователя в журнал.                                      ' \
                 '                   \n ' \
                 '1.3. Добавить задачу - добавить задачу в журнал.                                                  ' \
                 '                               \n' \
                 'ВАЖНО: Чтобы добавить задачув журнал, убедитесь, что его категория и ответственный\n уже добавлены ' \
                 'в систему, иначе задача не будет добавлен в систему.                                   \n ' \
                 '1.4 Посмотреть пользователей - откроет окно просмотра информации о всех пользователях.       \n ' \
                 '2. Поиск.                                                                                         ' \
                 '                                                            \n ' \
                 '2.1 Поиск по категории - выведет все задачи из этой категории.                                    ' \
                 '                    \n' \
                 '2.2. Поиск по ответственному - выведет все, что есть принадлежит данному человеку.                 \n' \
                 '2.3. Поиск по названию задачи - будет искать совпадения в графе задачи.                            ' \
                 '           \n ' \
                 '3. Печать - в директории, в которой расположено приложение, будет создан текстовый                \n' \
                 'документ с той информацией, выгрузку которой вы выбрали.                                        ' \
                 '             \n ' \
                 '4. Обновить - обновить информацию в таблице.                                                      ' \
                 '                             \n ' \
                 '5. Редактировать - если хотите изменить информацию в задаче в таблице, просто выделите         \n' \
                 'строку с нужной задачей и кликнете по клавише ИЗМЕНИТЬ.                                          ' \
                 '          \n' \
                 '6. Удалить - если вам надо удалить задачу, то выделите ее в таблице и нажмите УДАЛИТЬ.        \n' \
                 'Так же можно ' \
                 'выделить сразу несколько строк.'

        label_1 = tk.Label(frame_1,
                           text=poetry,
                           bg="#48466d",
                           fg="#bad7df",
                           font="Times 15")
        label_1.pack(side=TOP)


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
            filedata = file.read()

        filedata = filedata.replace('),', '. \n')
        filedata = filedata.replace('[', ' ')
        filedata = filedata.replace("'", ' ')
        filedata = filedata.replace(',', ' --- ')
        filedata = filedata.replace('(', '')
        filedata = filedata.replace(')', '')
        filedata = filedata.replace(']', '')

        with open('выгрузка_задачи.txt', 'w+') as file:
            file.write(filedata)


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
            filedata = file.read()

        filedata = filedata.replace('),', '. \n')
        filedata = filedata.replace('[', ' ')
        filedata = filedata.replace("'", ' ')
        filedata = filedata.replace(',', ' --- ')
        filedata = filedata.replace('(', '')
        filedata = filedata.replace(')', '')
        filedata = filedata.replace(']', '')

        with open('выгрузка_пользователей.txt', 'w+') as file:
            file.write(filedata)


if __name__ == "__main__":
    """Запуск приложения"""
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Задачи")
    root.geometry("1400x650+100+100")
    root.config(bg="#323232")
    root.mainloop()
