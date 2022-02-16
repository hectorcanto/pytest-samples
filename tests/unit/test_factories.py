from factory import StubFactory, DictFactory, Factory, fuzzy
from typing import NamedTuple
import factory

import pytest

class ObjectFactory(StubFactory):
    name: str = "value"


class NameDictFactory(DictFactory):
    name: str = "dict_factory"


class Simple(NamedTuple):
    style: str
    color: str


class SimpleFactory(Factory):
    class Meta:
        model = Simple

    style = factory.Faker("text")
    color = fuzzy.FuzzyChoice(["red", "green", "blue"])


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


@pytest.mark.current
def test_batch_factories():
    """Demo how to generate in batches"""

    two = SimpleFactory.create_batch(style="same", size=2)
    # both factories will have the same style
    assert two[0].style == "same"
    assert two[1].style == "same"

    another_two = SimpleFactory.create_batch(style="cool", color=factory.Iterator(["red", "blue"]), size=4)
    # all objects will have a `cool` style, and specific colors (not random)
    assert another_two[0].color == "red"
    assert another_two[1].color == "blue"
    assert another_two[3].color == "blue"
