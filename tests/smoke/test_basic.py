from source import SystemUnderTest
import pytest


@pytest.mark.first
def test_instantiation():
    SystemUnderTest()


def test_simplest():
    # set up
    entry = 1
    expected = 2
    sut = SystemUnderTest()
    # execution
    result = sut.function(input)
    # assertion
    assert result == expected


@pytest.mark.xfail(reason="raises an exception", run=True)
def test_with_extra_info():
    # set up
    entry = "1"
    expected = 2
    sut = SystemUnderTest()
    # execution
    result = sut.function(entry)
    # assertion
    assert result == expected, "Function should return double of the value "


@pytest.fixture(scope="module", name="sut")
def system_under_test():
    # setup
    instance = SystemUnderTest()
    yield instance.function
    # tear down
    del instance


@pytest.mark.parametrize("entry, expected", (
    (0, 0),
    (1, 2),
    (2, 4),
))
def test_with_params(sut, entry, expected):
    result = sut(entry)
    assert result == expected, "Function should return double"
