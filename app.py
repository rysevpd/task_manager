import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from database import DB
from admin_panel import AdminPanel

"""
https://colorhunt.co/palette/225739
"""

class Main(tk.Frame):
    """Основное окно программы."""

    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        sign_in = tk.Button(bg='#00587a',
                            fg='#ffffff',
                            text=' ВХОД ',
                            compound=tk.TOP,
                            font='Times 15',
                            command=self.open_dialog,
                            width=20)
        sign_in.pack(padx=5, pady=5)

        close = tk.Button(bg='#00587a',
                          fg='#ffffff',
                          text=' ЗАКРЫТЬ ',
                          compound=tk.TOP,
                          font='Times 15',
                          command=root.quit,
                          width=20)
        close.pack(padx=5, pady=5)

    def open_dialog(self):
        Dialog()

    def admin_menu(self):
        AdminPanel.init_main
        print('efefeff')

    def avtorize(self, login, pas):
        conn = sqlite3.connect('manager.db')
        c = conn.cursor()
        name_user = c.execute('''SELECT name FROM users
                    WHERE login =?''', (login,))
        name_user.fetchall()

        name_pas = c.execute('''SELECT name FROM users
                    WHERE pas =?''', (pas,))
        name_pas.fetchall()
        if name_user != name_pas:
            print(0)

        else:
            c = c.execute('''SELECT role FROM users
                        WHERE login =?''', (login,))
            c = str(c.fetchall())

            print(c)
            if c == "[('admin',)]":
                print(1)
                os.system('python admin_panel.py')
                # os.system('python main.py')
            else:
                # os.system('python main_1.py')
                print(2)

"""
class AdminPanel(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db

    def init_main(self):

        self.master = Tk()
        self.master.wm_state('zoomed')
        self.master.attributes("-topmost", True)
        self.master.geometry("600x450+300+300")
        self.master.title("Простое меню")
        self.master.config(bg="#e7e7de")

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        search_menu = Menu(menubar, tearoff=0)
        print_menu = Menu(menubar, tearoff=0)
        # file_menu.add_command(label="Выход")
        # menubar.add_cascade(label="Файл", menu=file_menu)

        search_menu.add_command(label="Поиск по задаче" #command=self.search_tasks
                                 )
        search_menu.add_command(label="Поиск по категории" #command=self.search_category
                                 )
        search_menu.add_command(label="Поиск по ответсвенному" # command=self.search_user
                                 )

        file_menu.add_command(label="Добавить категорию" #command=self.add_category
                              )  # command=self.add_rack
        file_menu.add_command(label="Добавить пользователя" #command=self.add_user
                               )  # command=self.add_provider
        file_menu.add_command(label="Добавить задачу" #command=self.add_task
                               )  # command=self.open_dialog
        file_menu.add_command(label="Показать пользователей"#command=self.list_users
                               )

        print_menu.add_command(label="Печать задач" # command=self.print_data
                                )
        print_menu.add_command(label="Печать пользователей" #command=self.print_users
                                )

        menubar.add_cascade(label="Фаил", menu=file_menu)
        menubar.add_cascade(label="Поиск", menu=search_menu)
        menubar.add_command(label="Помощь" #command=self.open_help_dialog
                             )
        menubar.add_cascade(label="Печать", menu=print_menu)
        menubar.add_command(label="Обновить" #command=self.view_records
                             )
        frame_1 = LabelFrame(self.master,
                             text="Управление",
                             bg="#008891")
        frame_1.pack(side=RIGHT, padx=10, fill=Y)
        # label_password = tk.Label(frame_1, text="пароль:", bg="#e7e7de", font='Times 15')
        # label_password.pack(side=TOP, padx=30, pady=1)

        update_data = tk.Button(frame_1,
                                text='Редактировать',
                                bg="#845ec2",
                                bd=2,
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
                               font='Times 15', command=root.destroy())
        exit_program.pack(side=BOTTOM, padx=5, pady=5)

        self.master.mainloop()
"""

class Dialog(tk.Toplevel):

    def __init__(self):
        super().__init__()
        # self.init_listusers()
        self.view = app
        # self.db = db
        db = DB()
        self.init_avtoriz()

    def init_avtoriz(self):
        root.destroy()
        ak = tk.Tk()
        ak.title("вход")
        ak.geometry("450x300+300+200")
        ak.config(bg="#e7e7de")

        frame_1 = Frame(ak, bg="#e7e7de")
        frame_1.pack(fill=X)

        label_login = tk.Label(frame_1, text="логин:  ", bg="#e7e7de", font='Times 15')
        label_login.pack(side=LEFT, padx=5, pady=5)

        entry_login = Entry(frame_1, justify="right")
        entry_login.pack(fill=X, padx=5, expand=True)

        frame_2 = Frame(ak, bg="#e7e7de")
        frame_2.pack(fill=X)

        label_password = tk.Label(frame_2, text="пароль:", bg="#e7e7de", font='Times 15')
        label_password.pack(side=LEFT, padx=5, pady=5)
        entry_password = Entry(frame_2, justify="right")
        entry_password.pack(fill=X, padx=5, expand=True)

        frame_3 = Frame(ak, bg="#e7e7de")
        frame_3.pack(fill=X)

        btn_cancel = tk.Button(frame_3,
                               bg='#00587a',
                               fg='#ffffff',
                               text=' ЗАКРЫТЬ ',
                               compound=tk.TOP,
                               font='Times 13',
                               command=ak.quit,
                               width=20)

        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

        btn_ok = tk.Button(frame_3,
                           bg='#00587a',
                           fg='#ffffff',
                           text=' ВХОД ',
                           compound=tk.TOP,
                           font='Times 13',
                           width=20)
        btn_ok.pack(side=LEFT, padx=5, pady=5)

        frame_4 = Frame(ak, bg="#e7e7de")
        frame_4.pack(fill=X)

        poetry = "Делать две вещи одновременно — означает не сделать ни одной." \
                 "\n© Публиус Сирус"
        label = tk.Label(frame_4,
                         text=poetry,
                         bg="#e7e7de")
        label.pack(side=BOTTOM, padx=2, pady=9)

        btn_ok.bind('<Button-1>', lambda event: self.view.avtorize(entry_login.get(),
                                                                   entry_password.get()))

        # btn_ok.bind('<Button-1>', lambda event: self.destroy())

        ak.mainloop()


if __name__ == "__main__":
    """Запуск приложения"""
    db = DB()

    root = tk.Tk()
    poetry = "Добро пожаловать в TASK MANAGER\n" \
             "Время — это то, чего мы хотим больше всего и то,\n " \
             "что мы хуже всего умеем использовать. - © Вильям Пенн"
    label2 = tk.Label(text=poetry,
                      bg="#e7e7de")
    label2.pack(padx=2, pady=7)
    root.config(bg="#e7e7de")
    app = Main(root)
    app.pack()

    root.title("Менеджер задач")
    root.geometry("450x300+300+200")
    root.resizable(False, False)
    root.mainloop()
