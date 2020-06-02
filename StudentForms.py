""" Экраны студента """
from collections import namedtuple
from tkinter import messagebox as mb, ttk
import tkinter as tk
import random
question = namedtuple('Question', ['id', 'question', 'A1', 'A2', 'A3', 'A4', 'correct'])


class StartTestingForm(tk.Toplevel):
    def __init__(self, master, grade_book_id, test_id):
        super().__init__(master)
        self.master = master
        self.grade_book_id = grade_book_id
        self.test_id = test_id
        self.db = master.db
        self.grab_set()
        self.focus_set()
        self.init_child()

    def init_child(self):
        self.title('Тест')
        self.geometry('600x200+440+340')
        self.resizable(False, False)
        self.questions = []
        self.questions_list = ""
        self.correct_list = ""
        self.points = 0
        self.generate_variant()
        self.start_testing()

    def start_testing(self):
        self.curr_index = 0
        self.view_question()

    def view_question(self):
        """Отображает на экране текущий вопрос"""
        self.curr_question = self.questions[self.curr_index]
        if self.curr_question != self.questions[-1]:
            self.btn = ttk.Button(self, text='Следующий вопрос', command=self.answer)
        else:
            self.btn = ttk.Button(self, text='Завершить тестирование', command=self.answer)
        self.btn.place(x=20, y=170)

        self.label = tk.Label(self, text=self.curr_question.question)
        self.label.place(x=20, y=20)
        self.var = tk.IntVar()
        self.var.set(0)
        self.A1 = tk.Radiobutton(self, text=self.curr_question.A1, variable=self.var, value=1)
        self.A2 = tk.Radiobutton(self, text=self.curr_question.A2, variable=self.var, value=2)
        self.A3 = tk.Radiobutton(self, text=self.curr_question.A3, variable=self.var, value=3)
        self.A4 = tk.Radiobutton(self, text=self.curr_question.A4, variable=self.var, value=4)

        self.A1.place(x=20, y=70)
        self.A2.place(x=20, y=90)
        self.A3.place(x=20, y=110)
        self.A4.place(x=20, y=130)

    def answer(self):
        self.btn.destroy()
        self.label.destroy()
        self.A1.destroy()
        self.A2.destroy()
        self.A3.destroy()
        self.A4.destroy()
        self.questions_list += str(self.curr_question.id)
        if self.var.get() == int(self.curr_question.correct):
            self.correct_list += str(self.curr_question.id)
            self.points += 1
        self.curr_index += 1
        if self.curr_index == len(self.questions):
            self.end_testing()
        else:
            self.view_question()

    def generate_variant(self):
        """Создает вариант тестирования для студента"""
        self.db.cursor.execute('''SELECT id, question, A1, A2, A3, A4, correct FROM QUESTIONS
                  WHERE test_id=?;''',
                               (str(self.test_id)))
        [self.questions.append(question(*row)) for row in self.db.cursor.fetchall()]
        random.shuffle(self.questions)

    def end_testing(self):
        """Завершает текущий тест, считает отметку, сохраняет вариант в системе, обновляет запись в журнале"""
        mb.showinfo(message='Тестирование завершено')
        grade = int((self.points / len(self.questions)) * 10)
        self.db.save_variant(self.questions_list, self.correct_list, self.points, self.grade_book_id)
        self.db.rate_test(self.grade_book_id, grade)
        self.master.student_view_records()
        self.destroy()


class ViewGradeBookForm(tk.Toplevel):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.master = master
        self.student_id = student_id
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
        self.title('Журнал учащегося')
        self.geometry('830x300+420+220')
        self.resizable(False, False)

        self.students_tree = ttk.Treeview(self, columns=('id', 'subject', 'topic', 'status', 'variant_id', 'grade'),
                                          height=8, show='headings')
        self.students_tree.column('id', width=120, anchor=tk.CENTER)
        self.students_tree.column('subject', width=120, anchor=tk.CENTER)
        self.students_tree.column('topic', width=170, anchor=tk.CENTER)
        self.students_tree.column('status', width=120, anchor=tk.CENTER)
        self.students_tree.column('variant_id', width=130, anchor=tk.CENTER)
        self.students_tree.column('grade', width=120, anchor=tk.CENTER)

        self.students_tree.heading('id', text='№ тестирования')
        self.students_tree.heading('subject', text='Предмет')
        self.students_tree.heading('topic', text='Тема')
        self.students_tree.heading('status', text='Статус теста')
        self.students_tree.heading('variant_id', text='Вариант теста')
        self.students_tree.heading('grade', text='Отметка')

        self.students_tree.place(x=20, y=90)
        self.scrollbar_students = tk.Scrollbar(self)
        self.scrollbar_students.place(x=815, y=120)
        # первая привязка
        self.scrollbar_students['command'] = self.students_tree.yview
        # вторая привязка
        self.students_tree['yscrollcommand'] = self.scrollbar_students.set

        # Заполнение таблицы данными
        self.view_marks()

    def view_marks(self):
        self.db.cursor.execute('''SELECT grade_book.id, tests.subject, tests.topic, grade_book.status, grade_book.variant_id, grade_book.grade
         FROM GRADE_BOOK AS grade_book
          JOIN TESTS AS tests ON tests.id = grade_book.test_id
          WHERE grade_book.student_id = ?
          ''', (self.student_id,))
        [self.students_tree.delete(i) for i in self.students_tree.get_children()]
        [self.students_tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]


