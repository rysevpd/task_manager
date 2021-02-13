import os
import tkinter as tk
from tkinter import ttk, Menu, Text




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
        




if __name__ == "__main__":
    """Запуск приложения"""
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