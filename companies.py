import random
import faker


class Company:
    id: int
    name: str
    year: int
    country: str

    def __init__(self, name: str, year: int, country: str, id: int = -1):
        self.id = id
        self.name = name
        self.year = year
        self.country = country

    @staticmethod
    def from_dict(raw: dict):
        return Company(id=raw['id'],
                       name=raw['name'],
                       year=raw['year'],
                       country=raw['country']
                       )
    @staticmethod
    def random_company():
        fake = faker.Faker('ru_RU')
        return Company(name=fake.company(),
                       year=random.randint(1940, 2020),
                       country=fake.country())

    def dict(self) ->dict[str, str]:
        return {
            'name': self.name,
            'year': self.year,
            'country': self.country
        }