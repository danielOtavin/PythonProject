import sqlite3
from enum import Enum


class TableName(Enum):
    USER =  'user'
    EMPLOYEE = 'employee'
    COMPANY = 'company'

class DB:
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.script_dict = {'user': "DELETE FROM user WHERE login != 'admin'",
                       'employee': "DELETE FROM employee",
                       'company': "DELETE FROM company"}

    def clean_table(self, table_name: TableName):
        script = self.script_dict[table_name.value]
        self.cursor.execute(script)
        self.conn.commit()

    def check_object_in_db(self, table_name: TableName, obj_id: int):
        self.cursor.execute(f'SELECT * FROM {table_name.value} WHERE id = ?', (obj_id,))
        result = self.cursor.fetchall()
        return result

    # def delete_obj(self, ):


