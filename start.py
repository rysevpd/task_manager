import os
import sys
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk, Menu, Text
import sqlite3
from main import DB


class Main(tk.Frame):
    """Основное окно программы."""

    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        # self.db = db

    def init_main(self):
        update_data = tk.Button(bg='#0d7377',
                                fg='#bad7df',
                                text=' ВХОД ',
                                compound=tk.TOP,
                                font='Times 15',
                                command=self.open_dialog,
                                width=20)
        update_data.pack(padx=5, pady=5)

        update_data_1 = tk.Button(bg='#0d7377',
                                  fg='#bad7df',
                                  text=' ЗАКРЫТЬ ',
                                  compound=tk.TOP,
                                  font='Times 15',
                                  command=root.quit,
                                  width=20)
        update_data_1.pack(padx=5, pady=5)
        # update_data.destroy()

    def open_dialog(self):

        Dialog()

    def avtorize(self, login, pas):
        conn = sqlite3.connect('manager.db')
        c = conn.cursor()
        x = c.execute('''SELECT name FROM users
                    WHERE login =?''', (login,))
        x = str(x.fetchall())

        y = c.execute('''SELECT name FROM users
                    WHERE pas =?''', (pas,))
        y = str(y.fetchall())
        if x != y:
            #print(0)
            l = 1

        else:
            c = c.execute('''SELECT role FROM users
                        WHERE login =?''', (login,))
            c = str(c.fetchall())
            #print(c)
            if c == "[('admin',)]":
                #print(1)
                os.system('python main.py')
                sys.exit()
            else:

                os.system('python main_1.py')
                #print(2)
                sys.exit()


class Dialog(tk.Toplevel):

    def __init__(self):
        super().__init__(root)
        # self.init_listusers()
        self.view = app
        self.db = db
        self.init_avtoriz()

    def init_avtoriz(self):
        self.title('вход')
        self.geometry("450x300+300+200")
        self.resizable(False, False)
        self.config(bg="#48466d")

        frame_1 = Frame(self, bg="#48466d")
        frame_1.pack(fill=X)
        label_login = tk.Label(frame_1, text="логин:  ", bg="#48466d", fg="#bad7df", font='Times 15')
        label_login.pack(side=LEFT, padx=5, pady=5)
        self.entry_login = Entry(frame_1, justify="right")
        self.entry_login.pack(fill=X, padx=5, expand=True)

        frame_2 = Frame(self, bg="#48466d")
        frame_2.pack(fill=X)
        label_pas = tk.Label(frame_2, text="пароль:", bg="#48466d", fg="#bad7df", font='Times 15')
        label_pas.pack(side=LEFT, padx=5, pady=5)
        self.entry_pas = Entry(frame_2, justify="right")
        self.entry_pas.pack(fill=X, padx=5, expand=True)

        frame_3 = Frame(self, bg="#48466d")
        frame_3.pack(fill=X)
        btn_cancel = tk.Button(frame_3,
                               bg='#0d7377',
                               fg='#bad7df',
                               text=' ЗАКРЫТЬ ',
                               compound=tk.TOP,
                               font='Times 13',
                               command=self.destroy,
                               width=20)
        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

        self.btn_ok = tk.Button(frame_3,
                                bg='#0d7377',
                                fg='#bad7df',
                                text=' ВХОД ',
                                compound=tk.TOP,
                                font='Times 13',
                                width=20)
        self.btn_ok.pack(side=LEFT, padx=5, pady=5)

        frame_4 = Frame(self, bg="#48466d")
        frame_4.pack(fill=X)

        poetry = "Делать две вещи одновременно — означает не сделать ни одной." \
                 "\n© Публиус Сирус"
        label = tk.Label(frame_4,
                         text=poetry,
                         bg="#48466d",
                         fg='#bad7df')
        label.pack(side=BOTTOM, padx=2, pady=9)

        self.btn_ok.bind('<Button-1>', lambda event: self.view.avtorize(self.entry_login.get(),
                                                                        self.entry_pas.get()))

        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')


if __name__ == "__main__":
    """Запуск приложения"""
    root = tk.Tk()
    db = DB()
    poetry = "Добро пожаловать в TASK MANAGER\n" \
             "Время — это то, чего мы хотим больше всего и то,\n " \
             "что мы хуже всего умеем использовать.\n© Вильям Пенн"
    label2 = tk.Label(text=poetry,
                      bg="#48466d",
                      font="Times 13",
                      fg="#bad7df")
    label2.pack(padx=2, pady=7)
    root.config(bg="#48466d")
    app = Main(root)
    app.pack()
    root.title("Запуск приложения")
    root.geometry("450x300+300+200")
    root.resizable(False, False)
    root.mainloop()
