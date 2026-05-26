import faker


class User:
    id: int
    login: str
    password: str
    
    @staticmethod
    def from_dict(raw: dict):
        return User(
            id=raw['id'],
            login= raw['login'],
            password=raw['password'],
        )
    
    @staticmethod
    def random_user():
        fake = faker.Faker('ru_RU')
        return User(login=fake.email(), password=fake.password(length=12))

    def __init__(self,login: str, password: str, id: int = -1):
        self.id = id
        self.login = login
        self.password = password

    def dict(self) -> dict[str, str]:
        return {
            "login": self.login,
            "password": self.password,
        }




ADMIN = User(login="admin", password="admin", id=1)
TEST = User(login="example@mail.ru", password="some_long_password1234@@$_")
ERROR = User(login="<unkown>", password="")

