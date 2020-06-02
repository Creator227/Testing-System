import sqlite3
from collections import namedtuple
User = namedtuple('User', ['id', 'name', 'status'])


class System_DB:
    def __init__(self):
        self.connection = sqlite3.connect('Testing_System.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''PRAGMA foreign_keys = ON;''')
        self.connection.commit()

    def _test_data_init(self):
        """Очищаем БД от лишних данных"""
        # В БД настроено каскадное удаление - после удаления таблицы
        # USERS автоматически удаляются все записи в остальных таблицах
        # Если необходимо удалить сами таблицы - удалить в порядке Variants, GradeBook, Questions, Tests, Users

        # self.cursor.execute(
        #     '''DROP TABLE IF EXISTS VARIANTS''')
        # self.cursor.execute(
        #     '''DROP TABLE IF EXISTS GradeBook''')
        # self.cursor.execute(
        #     '''DROP TABLE IF EXISTS QUESTIONS''')
        # self.cursor.execute(
        #     '''DROP TABLE IF EXISTS TESTS''')
        self.cursor.execute(
            '''DROP TABLE IF EXISTS USERS''')

        """ Заполнение БД тестовыми данными """
        self.cursor.execute(
            '''PRAGMA foreign_keys = ON;''')
        self.cursor.execute(
            ''' CREATE TABLE  IF NOT EXISTS USERS(
             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             password TEXT NOT NULL,
             status TEXT NOT NULL DEFAULT 'STUDENT');
        ''')
        self.cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS TESTS(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            test_time INTEGER NOT NULL,
            FOREIGN KEY(teacher_id) REFERENCES USERS(id)
            ON DELETE CASCADE
        );''')
        self.cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS QUESTIONS(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            A1 TEXT NOT NULL,
            A2 TEXT NOT NULL,
            A3 TEXT,
            A4 TEXT,
            correct INTEGER,
            FOREIGN KEY(test_id) REFERENCES TESTS(id) ON DELETE CASCADE
        );''')
        self.cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS GRADE_BOOK(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            status INT NOT NULL DEFAULT 0,
            variant_id INT,
            grade REAL,
            FOREIGN KEY(test_id) REFERENCES TESTS(id) ON DELETE CASCADE,
            FOREIGN KEY(student_id) REFERENCES USERS(id) ON DELETE CASCADE
        );''')
        self.cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS VARIANTS(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            questions_list TEXT NOT NULL,
            correct_list TEXT,
            points INT,
            grade_book_id INTEGER NOT NULL,
            FOREIGN KEY(grade_book_id) REFERENCES GRADE_BOOK(id) ON DELETE CASCADE
        );''')
        self.cursor.execute('''
            INSERT INTO USERS
            (name, password, status)
            VALUES
            ('Никита', '1823132', 'Администратор'),
            ('Алексей', '1823133', 'Преподаватель'),
            ('Иван', '1823134', 'Студент')
            ;
        ''')
        self.connection.commit()
    #############################################################

    def get_user(self, name: str, password: str) -> User:
        self.cursor.execute(
            ''' SELECT ID, NAME, STATUS FROM USERS
             WHERE NAME = ? AND PASSWORD = ?''', (name, password))
        user = self.cursor.fetchone()
        if not user:
            return User('', '', '')
        return User(user[0], user[1], user[2])

    def add_user(self, name: str, password: str, status: str):
        self.cursor.execute('''
                    INSERT INTO USERS
                    (name, password, status)
                    VALUES
                    (?, ?, ?);
                ''', (name, password, status))
        self.connection.commit()

    def delete_user(self, id: str):
        self.cursor.execute('''
                            DELETE FROM USERS
                            WHERE id = ?
                        ''', (id,))
        self.connection.commit()

    # Test methods

    def add_test(self, teacher_id: str, subject: str, topic: str, test_time):
        self.cursor.execute('''
                            INSERT INTO TESTS
                            (teacher_id, subject, topic, test_time)
                            VALUES
                            (?, ?, ?, ?);
                        ''', (teacher_id, subject, topic, test_time))
        self.connection.commit()

    def delete_test(self, id):
        self.cursor.execute('''
                            DELETE FROM TESTS
                            WHERE id = ?
                            ''', (id,))
        self.connection.commit()

    def update_test(self, id: int, teacher_id: int, subject: str, topic: str, test_time):
        self.cursor.execute('''
                              UPDATE TESTS
                              SET teacher_id = ?, subject = ?, topic = ?, test_time = ?
                              WHERE id = ?
                        ''', (teacher_id, subject, topic, test_time, id))
        self.connection.commit()

    # Question methods

    def add_question(self, test_id: int, question: str, A1: str, A2: str, A3: str, A4: str, correct):
        self.cursor.execute('''
                            INSERT INTO QUESTIONS
                            (test_id, question, A1, A2, A3, A4, correct)
                            VALUES
                            (?, ?, ?, ?, ?, ?, ?);
                         ''', (test_id, question, A1, A2, A3, A4, correct))
        self.connection.commit()

    def delete_question(self, id):
        self.cursor.execute('''
                              DELETE FROM TESTS
                              WHERE id = ?
                            ''', (id,))
        self.connection.commit()

    # Grade book methods

    def assign_test_to_student(self, test_id, student_id):
        self.cursor.execute('''
                                    INSERT INTO GRADE_BOOK
                                    (test_id, student_id)
                                    VALUES
                                    (?, ?);
                                 ''', (test_id, student_id))
        self.connection.commit()

    # Student methods

    def save_variant(self, questions_list, correct_list, points, grade_book_id):
        self.cursor.execute('''
                              INSERT INTO VARIANTS
                              (questions_list, correct_list, points, grade_book_id)
                              VALUES
                              (?, ?, ?, ?);
                            ''', (questions_list, correct_list, points, grade_book_id))
        self.connection.commit()

    def rate_test(self, grade_book_id, grade):
        self.cursor.execute('''
                            SELECT id FROM VARIANTS
                            WHERE grade_book_id = ?;
        ''', (grade_book_id,))
        row = self.cursor.fetchone()
        self.cursor.execute('''
                              UPDATE GRADE_BOOK
                              SET status='Пройден', grade=?, variant_id=?
                              WHERE id = ?
                            ''', (grade, row[0], grade_book_id))
        self.connection.commit()


if __name__ == '__main__':
    test = System_DB()
    test._test_data_init()


