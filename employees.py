import random
import faker
from pydantic import BaseModel

class Employee(BaseModel):
    id: int = -1
    name: str
    salary: int
    work: bool

    @staticmethod
    def random_employee():
        fake = faker.Faker('ru_RU')
        return Employee(
            name=fake.name(),
            salary=random.randint(1000, 5000),
            work=fake.boolean()
        )
