from datetime import datetime, timedelta, timezone
from enum import Enum
from random import randint
from typing import NamedTuple

import arrow
from factory import Factory, Faker, LazyAttribute, LazyFunction, SubFactory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyFloat, FuzzyText
from faker import Faker as FakeIt

from .dict_generator import generate_dict_factory

fake_it = FakeIt()  # Another way to use Faker


class Category(str, Enum):

    backend = "BackEnd"
    frontend = "FrontEnd"
    qa = "QA"

class Inner(NamedTuple):

    inner_value: float


class InnerFactory(Factory):

    inner = FuzzyFloat(1, 99.9)


class Structure(NamedTuple):
    # Could be Dataclass, Pydantic model or Marshmallow class
    # Could also a SQLAlchemy, Django or pyMongo model

    id: str # UUID
    active: bool
    value: int
    salary: float
    text: str
    category: str

    first_name: str
    last_name: str
    full_name: str
    username: str
    email: str
    password: str

    created_at: datetime
    updated_at: int

    nested: Inner


class StructureFactory(Factory):

    class Meta:
        model = Structure

    nested = SubFactory(InnerFactory)

    id = Faker("uuid4")
    active = True
    value = LazyFunction(lambda: randint(1, 1000))
    salary = FuzzyFloat(20_000, 50_000, 2)
    text = Faker("sentence", nb_words=5)
    category = FuzzyChoice(Category.__members__)

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    full_name = LazyAttribute(lambda self: self.first_name + " " + self.last_name)
    username = LazyAttribute(lambda self: self.full_name.replace(" ", "_"))
    email = LazyAttribute(lambda o: f'{o.username}@{fake_it.domain_name()}')
    password = FuzzyText(length=16)

    created_at = FuzzyDateTime(
        datetime.now(tz=timezone.utc) - timedelta(5 * 365),
        datetime.now(tz=timezone.utc) - timedelta(1 * 365),
    )
    updated_at = Faker(
        "unix_time",
        start_datetime=arrow.utcnow().shift(weeks=-3).date(),
        end_datetime=datetime.utcnow()
    )




StructureDictFactory = generate_dict_factory(StructureFactory)
