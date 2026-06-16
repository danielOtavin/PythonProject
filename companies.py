import random
import faker
from pydantic import BaseModel, StrictInt, StrictStr


class Company(BaseModel):
    id: StrictInt = -1
    name: StrictStr
    year: StrictInt
    country: StrictStr

    @staticmethod
    def random_company():
        fake = faker.Faker('ru_RU')
        return Company(name=fake.company(),
                       year=random.randint(1940, 2020),
                       country=fake.country())