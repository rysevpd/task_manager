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
        menubar.add_command(label="Обновить", command=self.view_records)

        frame_1 = LabelFrame(self.master, text="Управление", bg="#3d394d")
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
                             bg="#845ec2",
                             bd=2,
                             font='Times 15')
        del_data.pack(side=TOP, padx=5, pady=5)

        del_data = tk.Button(frame_1,
                             text='     Обновить   ',
                             bg="#845ec2",
                             bd=2,
                             font='Times 15')
        del_data.pack(side=TOP, padx=5, pady=5)

        programmer = tk.Button(frame_1,
                               text='О разработчике',
                               bg="#845ec2",
                               bd=2,
                               font='Times 15')
        programmer.pack(side=TOP, padx=5, pady=5)

        exit_program = tk.Button(frame_1,
                                 text='      Выход      ',
                                 bg="#845ec2",
                                 bd=2,
                                 font='Times 15', command=master.quit)
        exit_program.pack(side=BOTTOM, padx=5, pady=5)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11), foreground="#008891")  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'), bg="#008891")  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders)

        """Виджет tree - наша таблица"""
        frame_2 = LabelFrame(self.master,
                             text="Управление",
                             bg="#008891")
        frame_2.pack(side=LEFT, fill=BOTH)
        self.tree = ttk.Treeview(frame_2,
                                 style="mystyle.Treeview",
                                 columns=('task', 'category', 'status', 'responsible', 'date_start', 'date_end'),
                                 height=20,
                                 show='headings')

        self.tree.column('task', anchor=tk.CENTER)
        self.tree.column('category', anchor=tk.CENTER)
        self.tree.column('status', anchor=tk.CENTER)
        self.tree.column('responsible', anchor=tk.CENTER)
        self.tree.column('date_start', anchor=tk.CENTER)
        self.tree.column('date_end', anchor=tk.CENTER)

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
        self.title('Сотруники')
        self.geometry("950x450+300+200")
        self.resizable(False, False)

        update_data = tk.Button(self, text='Удалить сотрудника', bd=2, compound=tk.TOP,
                                command=self.delete_users)
        update_data.place(x=764, y=323)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=759, y=400)

        """Виджет tree - наша таблица"""

        self.tree = ttk.Treeview(self, columns=('name', 'login', 'pas', 'role', 'post', 'number', 'address'),
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
        self.geometry('400x420+400+300')
        self.resizable(False, False)

        label_user = tk.Label(self, text='Сотрудник:')
        label_user.place(x=50, y=50)
        label_login = tk.Label(self, text='Логин:')
        label_login.place(x=50, y=75)
        label_pas = tk.Label(self, text='Пароль:')
        label_pas.place(x=50, y=100)
        label_role = tk.Label(self, text='Роль:')
        label_role.place(x=50, y=125)
        label_post = tk.Label(self, text='Должность:')
        label_post.place(x=50, y=150)
        label_number = tk.Label(self, text='Номер телефона:')
        label_number.place(x=50, y=175)
        label_address = tk.Label(self, text='Адрес:')
        label_address.place(x=50, y=200)

        self.entry_user = ttk.Entry(self)
        self.entry_user.place(x=200, y=50)
        self.entry_login = ttk.Entry(self)
        self.entry_login.place(x=200, y=75)
        self.entry_pas = ttk.Entry(self)
        self.entry_pas.place(x=200, y=100)
        self.entry_post = ttk.Entry(self)
        self.entry_post.place(x=200, y=150)
        self.entry_number = ttk.Entry(self)
        self.entry_number.place(x=200, y=175)
        self.entry_address = ttk.Entry(self)
        self.entry_address.place(x=200, y=200)

        self.entry_role = ttk.Combobox(self, values=[u'admin', u'user'])
        self.entry_role.current(0)
        self.entry_role.place(x=200, y=125)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=225)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=225)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.record_user(self.entry_user.get(),
                                                                           self.entry_login.get(),
                                                                           self.entry_pas.get(),
                                                                           self.entry_role.get(),
                                                                           self.entry_post.get(),
                                                                           self.entry_number.get(),
                                                                           self.entry_address.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.grab_set()
        self.focus_set()


class Category(tk.Toplevel):
    """Окно добавления категории"""

    def __init__(self):
        super().__init__(master)
        self.init_category()
        self.view = app

    def init_category(self):
        self.title('Добавить категорию')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_category = tk.Label(self, text='Название категории:')
        label_category.place(x=50, y=50)

        self.entry_category = ttk.Entry(self)
        self.entry_category.place(x=200, y=50)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.record_category(self.entry_category.get()))

        self.grab_set()
        self.focus_set()


class Task(tk.Toplevel):
    """Окно добавления задачи"""

    def __init__(self):
        super().__init__(master)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить задачу')
        self.geometry('400x420+400+300')
        self.resizable(False, False)

        label_task = tk.Label(self, text='Задача:')
        label_task.place(x=50, y=50)
        label_category = tk.Label(self, text='Категория:')
        label_category.place(x=50, y=75)
        label_status = tk.Label(self, text='Статус:')
        label_status.place(x=50, y=100)
        label_responsible = tk.Label(self, text='Ответственный:')
        label_responsible.place(x=50, y=125)
        label_date_start = tk.Label(self, text='Старт задачи:')
        label_date_start.place(x=50, y=150)
        label_date_end = tk.Label(self, text='Срок до:')
        label_date_end.place(x=50, y=175)

        self.entry_task = ttk.Entry(self)
        self.entry_task.place(x=200, y=50)
        self.entry_category = ttk.Entry(self)
        self.entry_category.place(x=200, y=75)

        self.entry_status = ttk.Combobox(self, values=[u'TODO', u'in progress', u'suspended', u'DONE'])
        self.entry_status.current(0)
        self.entry_status.place(x=200, y=100)

        self.entry_responsible = ttk.Entry(self)
        self.entry_responsible.place(x=200, y=125)

        self.entry_date_start = ttk.Entry(self)
        self.entry_date_start.place(x=200, y=150)

        self.entry_date_end = ttk.Entry(self)
        self.entry_date_end.place(x=200, y=175)

        # self.entry_status = ttk.Combobox(self, values=[u'есть', u'отсутсвует'])
        # self.entry_status.current(0)
        # self.entry_status.place(x=200, y=110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=270)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=270)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_task.get(),
                                                                       self.entry_category.get(),
                                                                       self.entry_status.get(),
                                                                       self.entry_responsible.get(),
                                                                       self.entry_date_start.get(),
                                                                       self.entry_date_end.get()))

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
    # master.wm_state('zoomed')
    # master.attributes("-topmost", True)
    master.geometry("1200x650+100+100")
    master.title("Простое меню")
    master.config(bg="#e7e7de")
    app = AdminPanel(master)
    app.pack()
    master.mainloop()
