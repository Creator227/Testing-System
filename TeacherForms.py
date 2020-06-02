""" Экраны учителя """
from tkinter import ttk
import tkinter as tk


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
        self.geometry('400x180+440+340')
        self.resizable(False, False)

        label_subject = tk.Label(self, text='Предмет:')
        label_subject.place(x=50, y=40)

        label_topic = tk.Label(self, text='Тема:')
        label_topic.place(x=50, y=70)

        self.entry_subject = ttk.Entry(self)
        self.entry_subject.place(x=200, y=40)

        self.entry_topic = ttk.Entry(self)
        self.entry_topic.place(x=200, y=70)

        label_time = tk.Label(self, text='Время на выполнение:')
        label_time.place(x=50, y=100)
        self.combobox = ttk.Combobox(self, values=[u"30", u"45", u"80", u"120"])
        self.combobox.current(0)
        self.combobox.place(x=200, y=100)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=130)

        btn_ok = ttk.Button(self, text='Добавить', command=self.add_test)
        btn_ok.place(x=220, y=130)

    def add_test(self):
        self.db.add_test(self.master.user.id, self.entry_subject.get(), self.entry_topic.get(), self.combobox.get())
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


class UpdateTestForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = master.db
        self.init_child()
        self.grab_set()
        self.focus_set()

    def init_child(self):
        self.title('Изменить тест')
        self.geometry('400x220+440+340')
        self.resizable(False, False)

        label_id = tk.Label(self, text='ID теста')
        label_id.place(x=50, y=50)
        self.entry_id = ttk.Entry(self)
        self.entry_id.place(x=200, y=50)

        label_subject = tk.Label(self, text='Предмет:')
        label_subject.place(x=50, y=80)

        label_topic = tk.Label(self, text='Тема:')
        label_topic.place(x=50, y=110)

        self.entry_subject = ttk.Entry(self)
        self.entry_subject.place(x=200, y=80)

        self.entry_topic = ttk.Entry(self)
        self.entry_topic.place(x=200, y=110)

        label_time = tk.Label(self, text='Время на выполнение:')
        label_time.place(x=50, y=140)
        self.combobox = ttk.Combobox(self, values=[u"30", u"45", u"80", u"120"])
        self.combobox.current(0)
        self.combobox.place(x=200, y=140)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Обновить', command=self.update_test)
        btn_ok.place(x=220, y=170)

    def update_test(self):
        self.db.update_test(self.entry_id.get(), self.master.user.id, self.entry_subject.get(),
                            self.entry_topic.get(), self.combobox.get())
        self.master.teacher_view_records()


class ViewGradeBookForm(tk.Toplevel):
    def __init__(self, master, teacher_id):
        super().__init__(master)
        self.master = master
        self.teacher_id = teacher_id
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
        self.geometry('830x300+420+220')
        self.resizable(False, False)

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

        self.students_tree.place(x=20, y=60)
        self.scrollbar_students = tk.Scrollbar(self)
        self.scrollbar_students.place(x=815, y=120)
        # первая привязка
        self.scrollbar_students['command'] = self.students_tree.yview
        # вторая привязка
        self.students_tree['yscrollcommand'] = self.scrollbar_students.set
        self.students_tree.bind("<Double-1>", self.StudentsDoubleClick)
        # Заполнение таблицы данными
        self.view_students()

    def view_students(self):
        self.db.cursor.execute('''SELECT grade_book.id, grade_book.student_id, users.name, grade_book.status, grade_book.variant_id, grade_book.grade
         FROM GRADE_BOOK AS grade_book
          JOIN USERS AS users ON grade_book.student_id = users.id 
          ''')
        [self.students_tree.delete(i) for i in self.students_tree.get_children()]
        [self.students_tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    def StudentsDoubleClick(self):
        pass
