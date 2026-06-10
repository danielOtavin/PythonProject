import faker
from pydantic import BaseModel

class User(BaseModel):
    id: int = -1
    login: str
    password: str

    @staticmethod
    def random_user():
        fake = faker.Faker('ru_RU')
        return User(login=fake.email(), password=fake.password(length=12))





ADMIN = User(login="admin", password="admin", id=1)
TEST = User(login="example@mail.ru", password="some_long_password1234@@$_")
ERROR = User(login="<unkown>", password="")

