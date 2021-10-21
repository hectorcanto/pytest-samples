from datetime import date

from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyInteger

from source.models import User
from tests import common
from .dict_generator import generate_dict_factory


class UserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session = common.Session
        sqlalchemy_session_persistence = "flush"  # remember to commit
        # sqlalchemy_get_or_create = ("id",)

    id: int = FuzzyInteger(1, 2147483647)
    first_name: str = Faker("first_name")
    created_at: float = Faker("unix_time", start_datetime=date(2015, 1, 1), end_datetime=date(2019, 12, 31))


UserDictFactory = generate_dict_factory(UserFactory)
