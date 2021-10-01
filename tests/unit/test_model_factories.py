import factory
from factory import Faker, LazyFunction
from factory.alchemy import SQLAlchemyModelFactory
from source.models import User

from datetime import datetime


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
    id = 1
    first_name = Faker("first_name")
    created_at = LazyFunction(lambda: datetime(2021, 10, 2))


def test_model_factory():
    user = UserFactory.build()
    assert user.created_at == datetime(2021, 10, 2)


def test_model_factory_as_dict():

    my_dict = factory.build(dict, FACTORY_CLASS=UserFactory)
    assert isinstance(my_dict, dict)
    assert my_dict["id"] == 1

    another_dict = factory.build(dict, FACTORY_CLASS=UserFactory, first_name="Monty")
    assert another_dict["first_name"] == "Monty"
