import random
import faker

class Employee:
    name: str
    salary: int
    work: bool

    def __init__(self, name, salary, work):
        self.name = name
        self.salary = salary
        self.work = work

    @staticmethod
    def from_dict(raw: dict):
        return Employee(
            name = raw['name'],
            salary = raw['salary'],
            work = raw['work']
        )

    @staticmethod
    def random_employee():
        fake = faker.Faker('ru_RU')
        return Employee(
            name=fake.name(),
            salary=random.randint(1000, 5000),
            work=fake.boolean()
        )

    def dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "salary": self.salary,
            "work": self.work
        }

