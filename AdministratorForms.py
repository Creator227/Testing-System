""" Экраны администратора """
from tkinter import ttk
import tkinter as tk


class AddUserForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = master.db
        self.init_child()
        self.grab_set()
        self.focus_set()

    def init_child(self):
        self.title('Добавить пользователя')
        self.geometry('400x220+440+340')
        self.resizable(False, False)

        label_name = tk.Label(self, text='Имя пользователя:')
        label_name.place(x=50, y=50)

        label_sum = tk.Label(self, text='Пароль:')
        label_sum.place(x=50, y=110)

        label_status = tk.Label(self, text='Статус:')
        label_status.place(x=50, y=80)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_password = ttk.Entry(self)
        self.entry_password.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u"Студент", u"Учитель", u"Администратор"])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Добавить', command=self.add_user)
        btn_ok.place(x=220, y=170)

    def add_user(self):
        self.db.add_user(self.entry_name.get(), self.entry_password.get(), self.combobox.get())
        self.master.admin_view_records()


class DeleteUserForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = master.db
        self.init_child()
        self.grab_set()
        self.focus_set()

    def init_child(self):
        self.title('Удалить пользователя')
        self.geometry('400x220+440+340')
        self.resizable(False, False)

        label_id = tk.Label(self, text='Идентификатор пользователя:')
        label_id.place(x=40, y=50)

        self.entry_id = ttk.Entry(self)
        self.entry_id.place(x=220, y=50)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Удалить', command=self.delete_user)
        btn_ok.place(x=220, y=170)

    def delete_user(self):
        self.db.delete_user(self.entry_id.get())
        self.master.admin_view_records()
