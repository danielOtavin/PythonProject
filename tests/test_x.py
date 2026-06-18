import pytest
import sqlite3
from users import User
        
def test_x():
    con = sqlite3.connect("/Users/mac/Documents/projects/go/course-go/course.db")
    cursor = con.execute("select * from user where user.id=2")
    for user in cursor.fetchall():
        print(user)