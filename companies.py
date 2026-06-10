import random
import faker
from pydantic import BaseModel

class Company(BaseModel):
    id: int = -1
    name: str
    year: int
    country: str

    @staticmethod
    def random_company():
        fake = faker.Faker('ru_RU')
        return Company(name=fake.company(),
                       year=random.randint(1940, 2020),
                       country=fake.country())