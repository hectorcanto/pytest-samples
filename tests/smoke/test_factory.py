from tests.factories.models import UserDictFactory


def test_model_factory():
    user = UserDictFactory(first_name="John")
    assert user["first_name"] == "John"
