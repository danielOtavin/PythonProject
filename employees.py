import random
import faker
from pydantic import BaseModel, StrictStr, StrictInt


class Employee(BaseModel):
    id: StrictInt = -1
    name: StrictStr
    salary: StrictInt
    work: bool

    @staticmethod
    def random_employee():
        fake = faker.Faker('ru_RU')
        return Employee(
            name=fake.name(),
            salary=random.randint(1000, 5000),
            work=fake.boolean()
        )
