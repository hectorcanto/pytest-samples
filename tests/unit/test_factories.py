from factory import StubFactory, DictFactory, Factory
from typing import NamedTuple
import factory


class ObjectFactory(StubFactory):
    name: str = "value"


class NameDictFactory(DictFactory):
    name: str = "dict_factory"


class Simple(NamedTuple):
    style: str


class SimpleFactory(Factory):
    class Meta:
        model = Simple

    style = factory.Faker("text")


def test_stub_factory():
    my_object = ObjectFactory()
    assert my_object.name == "value"

    another_object = ObjectFactory(name="Guido")
    assert another_object.name == "Guido"


def test_dict_factory():
    my_dict = NameDictFactory()
    assert isinstance(my_dict, dict)
    assert my_dict["name"] == "dict_factory"


def test_named_tuple_factory():
    named_tuple = SimpleFactory(style="casual")
    assert named_tuple.style == "casual"