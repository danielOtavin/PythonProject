import faker
from pydantic import BaseModel, StrictInt, StrictStr

class User(BaseModel):
    id: StrictInt = -1
    login: StrictStr
    password: StrictStr

    @staticmethod
    def random_user():
        fake = faker.Faker('ru_RU')
        return User(
            login=f"{fake.user_name()}@{fake.domain_name()}.ru",
            password=fake.password(length=12)
        )





ADMIN = User(login="admin", password="admin", id=1)
TEST = User(login="example@mail.ru", password="some_long_password1234@@$_")
ERROR = User(login="<unkown>", password="")

