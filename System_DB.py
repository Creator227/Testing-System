import sqlite3
from collections import namedtuple
User = namedtuple('User', ['name', 'status'])


class System_DB:
    def __init__(self):
        self.connection = sqlite3.connect('Testing_System.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''PRAGMA foreign_keys = ON;''')
        self.connection.commit()


    def _test_data_init(self):
        """Очищаем БД от лишних данных"""
        self.cursor.execute(
            '''DROP TABLE IF EXISTS USERS''')
        self.cursor.execute(
            '''DROP TABLE IF EXISTS TESTS''')
        self.cursor.execute(
            '''DROP TABLE IF EXISTS QUESTIONS''')
        self.cursor.execute(
            '''DROP TABLE IF EXISTS VARIANTS''')
        self.cursor.execute(
            '''DROP TABLE IF EXISTS GradeBook''')
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
            FOREIGN KEY(test_id) REFERENCES TESTS(id)
        );''')
        self.cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS VARIANTS(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            questions_list TEXT NOT NULL,
            correct_list TEXT,
            points INT,
            FOREIGN KEY(test_id) REFERENCES TESTS(id),
            FOREIGN KEY(student_id) REFERENCES USERS(id)
            
        );''')
        self.cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS GradeBook(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            status INT NOT NULL DEFAULT 0,
            variant_id INT,
            grade REAL,
            FOREIGN KEY(test_id) REFERENCES TESTS(id),
            FOREIGN KEY(student_id) REFERENCES USERS(id)
        );''')
        self.cursor.execute('''
            INSERT INTO USERS
            (name, password, status)
            VALUES
            ('Никита', '12345678', 'Администратор'),
            ('Алексей', '12345678', 'Преподаватель'),
            ('Валерия', '12345678', 'Студент')
            ;
        ''')
        self.connection.commit()
    #############################################################

    def get_user(self, name: str, password: str) -> User:
        self.cursor.execute(
            ''' SELECT NAME, STATUS FROM USERS
             WHERE NAME = ? AND PASSWORD = ?''', (name, password))
        user = self.cursor.fetchone()
        if not user:
            return User('', '')
        return User(user[0], user[1])

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
                        ''', id)
        self.connection.commit()
    #############################################################

    def add_test(self, subject: str, topic: str, test_time):
        pass

    def delete_test(self, id):
        pass

    def update_test(self, id):
        pass


if __name__ == '__main__':
    test = System_DB()
    test._test_data_init()


