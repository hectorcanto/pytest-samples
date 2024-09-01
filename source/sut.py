from typing import Union

Numeric = Union[int, float]

class SystemUnderTest:

    def __init__(self):
        pass

    @staticmethod
    def function(value: Numeric|None) -> Numeric|None:
        """Function that returns the double of a numeric

        Returns:
            int or float depending on the input, None if None

        Raises:
            TypeError if unexpected type

        """
        if value is None:
            return None
        if not isinstance(value, (int, float)):
            raise TypeError("Expected numeric")
        return 2 * value

    @classmethod
    def raiser(cls, exc=ValueError, msg="raise on purpose"):
        raise exc(msg)
