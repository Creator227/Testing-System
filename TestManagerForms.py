import tkinter as tk
from tkinter import messagebox as mb, ttk
from System_DB import *


class TestManagerForm(tk.Toplevel):
    def __init__(self, master, test_id):
        super().__init__(master)
        self.master = master
        self.test_id = test_id
        self.db = master.db

        self.toolbar = tk.Frame(self, bg='#d7d8e0', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.img_logout = tk.PhotoImage(file='icons/Logout.gif')
        self.logout = tk.Button(self.toolbar, text='Назад', bg='#d7d8e0', bd=1, image=self.img_logout,
                                compound=tk.TOP, command=self.destroy)
        self.logout.pack(side=tk.RIGHT)

        self.init_child()
        self.grab_set()
        self.focus_set()

    def init_child(self):
        self.title('Информация о тесте')
        self.geometry('830x530+420+220')
        self.resizable(False, False)

        # Панель инструментов учителя
        self.img_add = tk.PhotoImage(file='icons/AddTest.gif')
        self.add_test = tk.Button(self.toolbar, text='Добавить вопрос', bg='#d7d8e0', bd=1, image=self.img_add,
                                  compound=tk.TOP, command=self.add_question)
        self.add_test.pack(side=tk.LEFT)

        self.assign = tk.PhotoImage(file='icons/Add.gif')
        self.assign_to_student_btn = tk.Button(self.toolbar, text='Назначить тест студенту', bg='#d7d8e0', bd=1,
                                               image=self.assign, command=self.assign_to_student, compound=tk.TOP, )
        self.assign_to_student_btn.pack(side=tk.LEFT)

        label_questions = tk.Label(self, text='Вопросы теста')
        label_questions.place(x=20, y=80)
        # Таблица с тестами для учителя
        self.questions_tree = ttk.Treeview(self, columns=('id', 'question', 'A1', 'A2', 'A3', 'A4', 'correct'),
                                           height=8, show='headings')
        self.questions_tree.column('id', width=30, anchor=tk.CENTER)
        self.questions_tree.column('question', width=150, anchor=tk.CENTER)
        self.questions_tree.column('A1', width=120, anchor=tk.CENTER)
        self.questions_tree.column('A2', width=120, anchor=tk.CENTER)
        self.questions_tree.column('A3', width=120, anchor=tk.CENTER)
        self.questions_tree.column('A4', width=120, anchor=tk.CENTER)
        self.questions_tree.column('correct', width=120, anchor=tk.CENTER)

        self.questions_tree.heading('id', text='ID')
        self.questions_tree.heading('question', text='Вопрос')
        self.questions_tree.heading('A1', text='Ответ 1')
        self.questions_tree.heading('A2', text='Ответ 2')
        self.questions_tree.heading('A3', text='Ответ 3')
        self.questions_tree.heading('A4', text='Ответ 4')
        self.questions_tree.heading('correct', text='Правильный ответ')
        self.questions_tree.place(x=20, y=100)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.place(x=815, y=150)
        # первая привязка
        self.scrollbar['command'] = self.questions_tree.yview
        # вторая привязка
        self.questions_tree['yscrollcommand'] = self.scrollbar.set
        self.questions_tree.bind("<Double-1>", self.QuestionsDoubleClick)
        # Заполнение таблицы данными
        self.view_questions()

        # Таблица со студентами, которым назначен тест
        label_students = tk.Label(self, text='Журнал тестирований учащихся')
        label_students.place(x=20, y=300)
        self.students_tree = ttk.Treeview(self, columns=('id', 'student_id', 'name', 'status', 'variant_id', 'grade'),
                                          height=8, show='headings')
        self.students_tree.column('id', width=120, anchor=tk.CENTER)
        self.students_tree.column('student_id', width=120, anchor=tk.CENTER)
        self.students_tree.column('name', width=170, anchor=tk.CENTER)
        self.students_tree.column('status', width=120, anchor=tk.CENTER)
        self.students_tree.column('variant_id', width=130, anchor=tk.CENTER)
        self.students_tree.column('grade', width=120, anchor=tk.CENTER)

        self.students_tree.heading('id', text='№ тестирования')
        self.students_tree.heading('student_id', text='ID студента')
        self.students_tree.heading('name', text='Имя студента')
        self.students_tree.heading('status', text='Стутус теста')
        self.students_tree.heading('variant_id', text='Вариант теста')
        self.students_tree.heading('grade', text='Отметка')

        self.students_tree.place(x=20, y=320)
        self.scrollbar_students = tk.Scrollbar(self)
        self.scrollbar_students.place(x=815, y=340)
        # первая привязка
        self.scrollbar_students['command'] = self.students_tree.yview
        # вторая привязка
        self.students_tree['yscrollcommand'] = self.scrollbar_students.set
        self.students_tree.bind("<Double-1>", self.StudentsDoubleClick)
        # Заполнение таблицы данными
        self.view_students()

    def QuestionsDoubleClick(self, event):
        if mb.askokcancel(title='Улаление вопросов',
                          message='Вы действительно хотите удалить выделенные вопросы?'):
            item = self.questions_tree.selection()[0]
            self.db.delete_question(self.questions_tree.item(item, 'values')[0])
            self.view_questions()

    def view_questions(self):
        self.db.cursor.execute('''SELECT id, question, A1, A2, A3, A4, correct FROM QUESTIONS WHERE test_id = ?''',
                               self.test_id)
        [self.questions_tree.delete(i) for i in self.questions_tree.get_children()]
        [self.questions_tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    def StudentsDoubleClick(self, event):
        pass
        # item = self.questions_tree.selection()[0]
        # self.db.delete_question(self.questions_tree.item(item, 'values')[0])
        # self.view_questions()

    def view_students(self):
        self.db.cursor.execute('''SELECT grade_book.id, grade_book.student_id, users.name, grade_book.status, grade_book.variant_id, grade_book.grade
         FROM GRADE_BOOK AS grade_book
          JOIN USERS AS users ON grade_book.student_id = users.id 
          WHERE test_id = ?''',
                               (self.test_id))
        [self.students_tree.delete(i) for i in self.students_tree.get_children()]
        [self.students_tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    def add_question(self):
        self.AddQuestionForm(self)

    class AddQuestionForm(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.db = master.db
            self.init_child()
            self.grab_set()
            self.focus_set()

        def init_child(self):
            self.title('Добавить вопрос')
            self.geometry('350x300+440+340')
            self.resizable(False, False)

            label_question = tk.Label(self, text='Вопрос:')
            label_question.place(x=20, y=40)
            self.entry_question = ttk.Entry(self, width=30)
            self.entry_question.place(x=75, y=40)

            label = tk.Label(self, text='Варианты ответов')
            label.place(x=20, y=70)

            label_a1 = tk.Label(self, text='1)')
            label_a1.place(x=20, y=100)
            self.entry_a1 = ttk.Entry(self)
            self.entry_a1.place(x=75, y=100)

            label_a2 = tk.Label(self, text='2)')
            label_a2.place(x=20, y=130)
            self.entry_a2 = ttk.Entry(self)
            self.entry_a2.place(x=75, y=130)

            label_a3 = tk.Label(self, text='3)')
            label_a3.place(x=20, y=160)
            self.entry_a3 = ttk.Entry(self)
            self.entry_a3.place(x=75, y=160)

            label_a4 = tk.Label(self, text='4)')
            label_a4.place(x=20, y=190)
            self.entry_a4 = ttk.Entry(self)
            self.entry_a4.place(x=75, y=190)

            label_correct = tk.Label(self, text='Правильный ответ:')
            label_correct.place(x=20, y=220)
            self.combobox = ttk.Combobox(self, values=[u"1", u"2", u"3", u"4"], width=20)
            self.combobox.current(0)
            self.combobox.place(x=150, y=220)

            btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
            btn_cancel.place(x=250, y=250)

            btn_ok = ttk.Button(self, text='Добавить', command=self.add_question)
            btn_ok.place(x=170, y=250)

        def add_question(self):
            self.db.add_question(self.master.test_id, self.entry_question.get(), self.entry_a1.get(),
                                 self.entry_a2.get(), self.entry_a3.get(), self.entry_a4.get(), self.combobox.get())
            self.master.view_questions()

    def assign_to_student(self):
        self.AssignForm(self)

    class AssignForm(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.db = master.db
            self.init_child()
            self.grab_set()
            self.focus_set()

        def init_child(self):
            self.title('Назначить тест студенту')
            self.geometry('480x190+440+340')
            self.resizable(False, False)

            # Таблица пользователей
            self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Password', 'Status'), height=5, show='headings')
            self.tree.column('ID', width=30, anchor=tk.CENTER)
            self.tree.column('Name', width=150, anchor=tk.CENTER)
            self.tree.column('Password', width=150, anchor=tk.CENTER)
            self.tree.column('Status', width=100, anchor=tk.CENTER)

            self.tree.heading('ID', text='ID')
            self.tree.heading('Name', text='Имя пользователя')
            self.tree.heading('Password', text='Пароль')
            self.tree.heading('Status', text='Статус')

            self.tree.place(x=20, y=20)

            self.scrollbar = tk.Scrollbar(self)
            self.scrollbar.pack(side='right')
            # первая привязка
            self.scrollbar['command'] = self.tree.yview
            # вторая привязка
            self.tree['yscrollcommand'] = self.scrollbar.set

            # Обработка нажатия на запись
            self.tree.bind("<Double-1>", self.OnDoubleClick)
            # Заполнение таблицы данными
            self.view_students()

            btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
            btn_cancel.place(x=380, y=150)

        def view_students(self):
            self.db.cursor.execute('''SELECT * FROM USERS WHERE status='Студент';''')
            [self.tree.delete(i) for i in self.tree.get_children()]
            [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

        def OnDoubleClick(self, event):
            item = self.tree.selection()[0]
            self.db.assign_test_to_student(self.master.test_id, self.tree.item(item, 'values')[0])
            self.master.view_students()

