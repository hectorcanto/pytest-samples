from functools import partial
from typing import Any, Dict, Union

from factory import Factory
from factory.base import StubObject, FactoryMetaClass


# from https://github.com/FactoryBoy/factory_boy/issues/68#issuecomment-636452903
def generate_dict_factory(the_factory: Union[StubObject, FactoryMetaClass]):
    """Usage:
    DictFactory = generate_dict_factory(MyFactory)
    my_dict = DictFactory()
    """
    def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
        stub_dict = stub.__dict__
        for key, value in stub_dict.items():
            if isinstance(value, StubObject):
                stub_dict[key] = convert_dict_from_stub(value)
        return stub_dict

    def dict_factory(stub_factory, **kwargs):
        stub = stub_factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, the_factory)
