import pytest

from source import SystemUnderTest


@pytest.mark.skip(reason="show skipped")
def test_instantiation():
    SystemUnderTest()


@pytest.mark.first
def test_instantiation():
    SystemUnderTest()


def test_simplest():
    # arrange
    entry = 1
    expected = 2
    sut = SystemUnderTest()
    # act
    result = sut.function(entry)
    # asert
    assert result == expected


def test_will_fail():
    result = SystemUnderTest().function(1)
    assert result == 4, "Function should return double of the value"


@pytest.mark.xfail(reason="raises an exception", run=True)
def test_with_extra_info():
    # set up
    entry = "1"
    expected = 2
    sut = SystemUnderTest()
    # execution
    result = sut.function(entry)
    # assertion
    assert result == expected


@pytest.fixture(scope="module", name="sut")
def system_under_test():
    # set up
    instance = SystemUnderTest()
    yield instance.function
    # tear down
    del instance


@pytest.mark.parametrize("entry, expected", (
    (0, 0),
    (1, 2),
    (2, 4),
    ),
    ids=['zero', 'one', 'two']
)
def test_with_params(sut, entry, expected):
    result = sut(entry)
    assert result == expected, "Function should return double"


def test_raise():
    with pytest.raises(ValueError) as exc_info:
        SystemUnderTest.raiser(msg="exception msg")

    assert str(exc_info.value) == "exception msg"

