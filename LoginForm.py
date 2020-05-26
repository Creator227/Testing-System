import tkinter as tk
from tkinter import messagebox as mb
from System_DB import *
from MainMenuForm import MainMenuForm


class LoginForm(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = System_DB()
        self.pack()
        self.master.title('Войти в систему')
        self.master.geometry('300x180+580+300')
        self.master.resizable(False, False)
        self.create_widgets()


    def create_widgets(self):
        self.text_log = tk.Label(self, text='Имя пользователя')
        self.user_login = tk.Entry(self)

        self.text_password = tk.Label(self, text='Пароль')
        self.user_password = tk.Entry(self, show='*')

        self.img_login = tk.PhotoImage(file='icons/Login.gif')
        self.button_log = tk.Button(self, text='Войти в систему', bd=0,
                                     compound=tk.TOP, image=self.img_login, command=self.login)

        self.text_log.pack()
        self.user_login.pack()
        self.text_password.pack()
        self.user_password.pack()
        self.button_log.pack()

    def login(self):
        user = self.db.get_user(self.user_login.get(), self.user_password.get())
        if user.status == '':
            mb.showerror('Невозможно войти', 'Проверьте введенные данные')
        else:
            MainMenuForm(self, user)

