import tkinter as tk
from tkinter import messagebox as mb, ttk
from System_DB import *


class ManageTestForm(tk.Toplevel):
    def __init__(self, master, test_id):
        super().__init__(master)
        self.master = master
        self.test_id = test_id
        self.db = master.db

        self.toolbar = tk.Frame(self, bg='#d7d8e0', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.init_child()
        self.grab_set()
        self.focus_set()
        self.grab_set()
        self.focus_set()

    def init_child(self):
        self.title('Вопросы теста')
        self.geometry('850x305+420+320')
        self.resizable(False, False)

        # Панель инструментов учителя
        self.img_add = tk.PhotoImage(file='icons/AddTest.gif')
        self.add_test = tk.Button(self.toolbar, text='Добавить вопрос', bg='#d7d8e0', bd=1, image=self.img_add,
                                  compound=tk.TOP, command=self.add_question)
        self.add_test.pack(side=tk.LEFT)

        self.img_delete = tk.PhotoImage(file='icons/DeleteTest.gif')
        self.delete_test = tk.Button(self.toolbar, text='Удалить вопрос', bg='#d7d8e0', bd=1,
                                     image=self.img_delete,
                                     compound=tk.TOP)
        self.delete_test.pack(side=tk.LEFT)

        # Таблица с тестами для учителя
        self.tree = ttk.Treeview(self, columns=('id', 'question', 'A1', 'A2', 'A3', 'A4', 'correct'), height=8, show='headings')
        self.tree.column('id', width=30, anchor=tk.CENTER)
        self.tree.column('question', width=150, anchor=tk.CENTER)
        self.tree.column('A1', width=120, anchor=tk.CENTER)
        self.tree.column('A2', width=120, anchor=tk.CENTER)
        self.tree.column('A3', width=120, anchor=tk.CENTER)
        self.tree.column('A4', width=120, anchor=tk.CENTER)
        self.tree.column('correct', width=150, anchor=tk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('question', text='Вопрос')
        self.tree.heading('A1', text='Ответ 1')
        self.tree.heading('A2', text='Ответ 2')
        self.tree.heading('A3', text='Ответ 3')
        self.tree.heading('A4', text='Ответ 4')
        self.tree.heading('correct', text='Правильный ответ')
        self.tree.place(x=20, y=100)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right')
        # первая привязка
        self.scrollbar['command'] = self.tree.yview
        # вторая привязка
        self.tree['yscrollcommand'] = self.scrollbar.set
        self.tree.bind("<Double-1>", self.OnDoubleClick)

        # Заполнение таблицы данными
        self.view_questions()

    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        self.db.delete_question(self.tree.item(item, 'values')[0])
        self.view_questions()

    def view_questions(self):
        self.db.cursor.execute('''SELECT id, question, A1, A2, A3, A4, correct FROM QUESTIONS WHERE test_id = ?''', (self.test_id))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

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
            self.geometry('400x300+440+340')
            self.resizable(False, False)

            label_question = tk.Label(self, text='Вопрос:')
            label_question.place(x=50, y=40)
            self.entry_question = ttk.Entry(self, width=30)
            self.entry_question.place(x=125, y=40)

            label = tk.Label(self, text='Варианты ответов')
            label.place(x=75, y=70)

            label_a1 = tk.Label(self, text='1)')
            label_a1.place(x=50, y=100)
            self.entry_a1 = ttk.Entry(self)
            self.entry_a1.place(x=75, y=100)

            label_a2 = tk.Label(self, text='2)')
            label_a2.place(x=50, y=130)
            self.entry_a2 = ttk.Entry(self)
            self.entry_a2.place(x=75, y=130)

            label_a3 = tk.Label(self, text='3)')
            label_a3.place(x=50, y=160)
            self.entry_a3 = ttk.Entry(self)
            self.entry_a3.place(x=75, y=160)

            label_a4 = tk.Label(self, text='4)')
            label_a4.place(x=50, y=190)
            self.entry_a4 = ttk.Entry(self)
            self.entry_a4.place(x=75, y=190)

            label_correct = tk.Label(self, text='Правильный ответ:')
            label_correct.place(x=50, y=220)
            self.combobox = ttk.Combobox(self, values=[u"1", u"2", u"3", u"4"])
            self.combobox.current(0)
            self.combobox.place(x=200, y=220)

            btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
            btn_cancel.place(x=300, y=250)

            btn_ok = ttk.Button(self, text='Добавить', command=self.add_question)
            btn_ok.place(x=220, y=250)

        def add_question(self):
            self.db.add_question(self.master.test_id, self.entry_question.get(), self.entry_a1.get(),
                                 self.entry_a2.get(), self.entry_a3.get(), self.entry_a4.get(), self.combobox.get())
            self.master.view_questions()

