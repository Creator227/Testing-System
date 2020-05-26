import tkinter as tk
from tkinter import messagebox as mb, ttk
from System_DB import *


class MainMenuForm(tk.Toplevel):
    def __init__(self, master, user: User):
        super().__init__(master)
        self.master = master
        self._root().withdraw()
        self.db = master.db

        self.grab_set()
        self.focus_set()
        self.toolbar = tk.Frame(self, bg='#d7d8e0', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.img_logout = tk.PhotoImage(file='icons/Logout.gif')
        self.logout = tk.Button(self.toolbar, text='Выйти', bg='#d7d8e0', bd=1, image=self.img_logout,
                                  compound=tk.TOP, command=self.logout)
        self.logout.pack(side=tk.RIGHT)

        # Тулбар буден у всех пользователей, но доступные элементы различны от прав
        if user.status == 'Администратор':
            self.init_administrators_menu()
        if user.status == 'Преподаватель':
            self.init_teachers_menu()
        if user.status == 'Студент':
            self.init_students_menu()

    def logout(self):
        self._root().deiconify()
        self.destroy()
    """ Методы для меню студента """
    def init_students_menu(self):
        pass

    """ Методы для меню преподавателя """
    def init_teachers_menu(self):
        self.title('Меню преподавателя')
        self.geometry('500x305+400+300')
        self.resizable(False, False)

        # Панель инструментов учителя
        self.img_add = tk.PhotoImage(file='icons/AddTest.gif')
        self.add_test = tk.Button(self.toolbar, text='Добавить тест', bg='#d7d8e0', bd=1, image=self.img_add,
                                  compound=tk.TOP, command=self.teacher_add_test)
        self.add_test.pack(side=tk.LEFT)

        self.img_update = tk.PhotoImage(file='icons/UpdateTest.gif')
        self.update_test = tk.Button(self.toolbar, text='Изменить тест', bg='#d7d8e0', bd=1,
                                     image=self.img_update,
                                     compound=tk.TOP, command=self.admin_delete_user)
        self.update_test.pack(side=tk.LEFT)

        self.img_delete = tk.PhotoImage(file='icons/DeleteTest.gif')
        self.delete_test = tk.Button(self.toolbar, text='Удалить тест', bg='#d7d8e0', bd=1,
                                     image=self.img_delete,
                                     compound=tk.TOP, command=self.admin_delete_user)
        self.delete_test.pack(side=tk.LEFT)

        self.img_grade = tk.PhotoImage(file='icons/GradeBook.gif')
        self.delete_test = tk.Button(self.toolbar, text='Журнал', bg='#d7d8e0', bd=1,
                                     image=self.img_grade,
                                     compound=tk.TOP, command=self.admin_delete_user)
        self.delete_test.pack(side=tk.LEFT)

    def teacher_add_test(self):
        self.AddTestForm(self)

    def teacher_update_test(self):
        pass

    def teacher_delete_test(self):
        pass

    class AddTestForm(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.db = master.db
            self.init_child()
            self.grab_set()
            self.focus_set()

        def init_child(self):
            self.title('Добавить тест')
            self.geometry('400x220+440+340')
            self.resizable(False, False)

            label_subject = tk.Label(self, text='Предмет:')
            label_subject.place(x=50, y=110)

            label_topic = tk.Label(self, text='Тема:')
            label_topic.place(x=50, y=80)

            self.entry_subject = ttk.Entry(self)
            self.entry_subject.place(x=200, y=50)

            self.entry_topic = ttk.Entry(self)
            self.entry_topic.place(x=200, y=110)

            self.combobox = ttk.Combobox(self, values=[u"30", u"45", u"80", u"120"])
            self.combobox.current(0)
            self.combobox.place(x=200, y=80)

            btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
            btn_cancel.place(x=300, y=170)

            btn_ok = ttk.Button(self, text='Добавить', command=self.add_test)
            btn_ok.place(x=220, y=170)

        def add_test(self):
            self.db.add_user(self.entry_subject.get(), self.entry_topic.get(), self.combobox.get())
            self.master.teacher_view_records()

    class DeleteTestForm(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.db = master.db
            self.init_child()
            self.grab_set()
            self.focus_set()

        def init_child(self):
            self.title('Удалить тест')
            self.geometry('400x220+440+340')
            self.resizable(False, False)

            label_id = tk.Label(self, text='Идентификатор теста:')
            label_id.place(x=40, y=50)

            self.entry_id = ttk.Entry(self)
            self.entry_id.place(x=220, y=50)

            btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
            btn_cancel.place(x=300, y=170)

            btn_ok = ttk.Button(self, text='Удалить', command=self.delete_test)
            btn_ok.place(x=220, y=170)

        def delete_test(self):
            self.db.delete_test(self.entry_id.get())
            self.master.teacher_view_records()
    """ Методы для меню администратора """
    def init_administrators_menu(self):
        self.title('Панель администратора')
        self.geometry('470x305+440+340')
        self.resizable(False, False)

        # Панель инструментов аминистратора
        self.img_add = tk.PhotoImage(file='icons/Add.gif')
        self.add_user = tk.Button(self.toolbar, text='Добавить пользователя', bg='#d7d8e0', bd=1, image=self.img_add,
                                   compound=tk.TOP, command=self.admin_add_user)
        self.add_user.pack(side=tk.LEFT)

        self.img_delete = tk.PhotoImage(file='icons/Delete.gif')
        self.delete_user = tk.Button(self.toolbar, text='Удалить пользователя', bg='#d7d8e0', bd=1, image=self.img_delete,
                                  compound=tk.TOP, command=self.admin_delete_user)
        self.delete_user.pack(side=tk.LEFT)

        # Таблица пользователей
        self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Password', 'Status'), height=8, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('Name', width=150, anchor=tk.CENTER)
        self.tree.column('Password', width=150, anchor=tk.CENTER)
        self.tree.column('Status', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Имя пользователя')
        self.tree.heading('Password', text='Пароль')
        self.tree.heading('Status', text='Статус')

        self.tree.place(x=20, y=100)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right')
        # первая привязка
        self.scrollbar['command'] = self.tree.yview
        # вторая привязка
        self.tree['yscrollcommand'] = self.scrollbar.set

        # Заполнение таблицы данными
        self.admin_view_records()

    def admin_view_records(self):
        self.db.cursor.execute('''SELECT * FROM USERS''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    def admin_add_user(self):
        self.AddUserForm(self)

    def admin_delete_user(self):
        self.DeleteUserForm(self)

    """ Экраны администратора """
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





