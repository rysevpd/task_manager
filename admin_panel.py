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
        #self.view_records()

    def init_main(self):
        menubar = Menu(master)
        master.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        search_menu = Menu(menubar, tearoff=0)
        print_menu = Menu(menubar, tearoff=0)

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
                               font='Times 15', command=master.quit)
        exit_program.pack(side=BOTTOM, padx=5, pady=5)

        """Виджет tree - наша таблица"""
        frame_2 = LabelFrame(self.master,
                             text="Управление",
                             bg="#008891")
        frame_2.pack(side=LEFT, padx=10, fill=BOTH)
        self.tree = ttk.Treeview(frame_2, columns=('ID', 'task', 'category', 'status', 'responsible', 'date_start',
                                                'date_end'), height=20, show='headings')

        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('task', width=250, anchor=tk.CENTER)
        self.tree.column('category', width=130, anchor=tk.CENTER)
        self.tree.column('status', width=150, anchor=tk.CENTER)
        self.tree.column('responsible', width=250, anchor=tk.CENTER)
        self.tree.column('date_start', width=150, anchor=tk.CENTER)
        self.tree.column('date_end', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='  ID  ')
        self.tree.heading('task', text='Задча')
        self.tree.heading('category', text='Категория')
        self.tree.heading('status', text='Статус')
        self.tree.heading('responsible', text='Ответственный')
        self.tree.heading('date_start', text='Начало')
        self.tree.heading('date_end', text='Срок')
        self.tree.pack(side=LEFT, pady=1, padx=1, fill=Y )
        #self.tree.pack()


if __name__ == "__main__":
    """Запуск приложения"""
    db = DB()
    master = Tk()
    master.wm_state('zoomed')
    master.attributes("-topmost", True)
    master.geometry("600x450+300+300")
    master.title("Простое меню")
    master.config(bg="#e7e7de")
    app = AdminPanel(master)
    app.pack()
    master.mainloop()

