import tkinter as tk
from tkinter import messagebox as mb, ttk

import AdministratorForms
import TeacherForms
import StudentForms
from System_DB import *
from TestManagerForms import TestManagerForm


class MainMenuForm(tk.Toplevel):
    def __init__(self, master, user: User):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = master.db

        self.grab_set()
        self.focus_set()
        self.toolbar = tk.Frame(self, bg='#d7d8e0', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.img_logout = tk.PhotoImage(file='icons/Logout.gif')
        self.logout = tk.Button(self.toolbar, text='Выйти', bg='#d7d8e0', bd=1, image=self.img_logout,
                                  compound=tk.TOP, command=self.logout)
        self.logout.pack(side=tk.RIGHT)

        # Тулбар будет у всех пользователей, но доступные элементы различны от прав
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
        self.title('Меню студента')
        self.geometry('625x305+400+300')
        self.resizable(False, False)
        self.img_grade = tk.PhotoImage(file='icons/GradeBook.gif')
        self.delete_test = tk.Button(self.toolbar, text='Мои оценки', bg='#d7d8e0', bd=1,
                                     image=self.img_grade,
                                     compound=tk.TOP, command=self.student_grade_book)
        self.delete_test.pack(side=tk.LEFT)
        # Таблица с непройденными назначенными студенту тестами
        self.student_tree = ttk.Treeview(self, columns=('id', 'test_id', 'subject', 'teachers_name', 'topic', 'test_time'), height=8, show='headings')
        self.student_tree.column('id', width=15, anchor=tk.CENTER)
        self.student_tree.column('test_id', width=50, anchor=tk.CENTER)
        self.student_tree.column('subject', width=140, anchor=tk.CENTER)
        self.student_tree.column('teachers_name', width=140, anchor=tk.CENTER)
        self.student_tree.column('topic', width=120, anchor=tk.CENTER)
        self.student_tree.column('test_time', width=120, anchor=tk.CENTER)

        self.student_tree.heading('id', text='ID')
        self.student_tree.heading('test_id', text='ID теста')
        self.student_tree.heading('subject', text='Предмет')
        self.student_tree.heading('teachers_name', text='ФИО преподавателя')
        self.student_tree.heading('topic', text='Тема')
        self.student_tree.heading('test_time', text='Время выполнения')

        self.student_tree.place(x=20, y=100)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right')
        # первая привязка
        self.scrollbar['command'] = self.student_tree.yview
        # вторая привязка
        self.student_tree['yscrollcommand'] = self.scrollbar.set
        self.student_tree.bind("<Double-1>", self.OnStudentTreeDoubleClick)

        # Заполнение таблицы данными
        self.student_view_records()

    def student_view_records(self):
        self.db.cursor.execute('''SELECT grade_book.id, tests.id, tests.subject, users.name, tests.topic, tests.test_time
         FROM GRADE_BOOK AS grade_book
         JOIN TESTS AS tests ON grade_book.test_id = tests.id
         JOIN USERS AS users ON tests.teacher_id = users.id 
          WHERE grade_book.student_id = ? AND grade_book.status='0'; ''',
                               (str(self.user.id)))
        [self.student_tree.delete(i) for i in self.student_tree.get_children()]
        [self.student_tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    def OnStudentTreeDoubleClick(self, event):
        if mb.askokcancel(title='Пройти тестирование', message='Вы готовы пройти тест? Тестирование начнется немедленно'):
            item = self.student_tree.selection()[0]
            StudentForms.StartTestingForm(self, self.student_tree.item(item, 'values')[0], self.student_tree.item(item, 'values')[1])

    def student_grade_book(self):
        StudentForms.ViewGradeBookForm(self, self.user.id)

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
                                     compound=tk.TOP, command=self.teacher_update_test)
        self.update_test.pack(side=tk.LEFT)

        self.img_delete = tk.PhotoImage(file='icons/DeleteTest.gif')
        self.delete_test = tk.Button(self.toolbar, text='Удалить тест', bg='#d7d8e0', bd=1,
                                     image=self.img_delete,
                                     compound=tk.TOP, command=self.teacher_delete_test)
        self.delete_test.pack(side=tk.LEFT)

        self.img_grade = tk.PhotoImage(file='icons/GradeBook.gif')
        self.delete_test = tk.Button(self.toolbar, text='Журнал', bg='#d7d8e0', bd=1,
                                     image=self.img_grade,
                                     compound=tk.TOP, command=self.teacher_grade_book)
        self.delete_test.pack(side=tk.LEFT)

        # Таблица с тестами для учителя
        self.tree = ttk.Treeview(self, columns=('id', 'subject', 'topic', 'test_time'), height=8, show='headings')
        self.tree.column('id', width=30, anchor=tk.CENTER)
        self.tree.column('subject', width=150, anchor=tk.CENTER)
        self.tree.column('topic', width=150, anchor=tk.CENTER)
        self.tree.column('test_time', width=120, anchor=tk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('subject', text='Предмет')
        self.tree.heading('topic', text='Тема')
        self.tree.heading('test_time', text='Время выполнения')

        self.tree.place(x=20, y=100)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right')
        # первая привязка
        self.scrollbar['command'] = self.tree.yview
        # вторая привязка
        self.tree['yscrollcommand'] = self.scrollbar.set
        self.tree.bind("<Double-1>", self.OnTeacherTreeDoubleClick)

        # Заполнение таблицы данными
        self.teacher_view_records()

    def OnTeacherTreeDoubleClick(self, event):
        item = self.tree.selection()[0]
        TestManagerForm(self, self.tree.item(item, 'values')[0])

    def teacher_view_records(self):
        self.db.cursor.execute('''SELECT id, subject, topic, test_time FROM TESTS WHERE teacher_id = ?''', (str(self.user.id)))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    def teacher_add_test(self):
        TeacherForms.AddTestForm(self)

    def teacher_update_test(self):
        TeacherForms.UpdateTestForm(self)

    def teacher_delete_test(self):
        TeacherForms.DeleteTestForm(self)

    def teacher_grade_book(self):
        TeacherForms.ViewGradeBookForm(self, self.user.id)

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
        AdministratorForms.AddUserForm(self)

    def admin_delete_user(self):
        AdministratorForms.DeleteUserForm(self)


