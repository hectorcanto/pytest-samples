from pytest import approx

from source.sut import SystemUnderTest

def test_with_approx():
    """Example with pytest.approx"""
    result = SystemUnderTest.function(2)

    assert result == approx(3.99, 4.01), "Result should be 4, within range"


