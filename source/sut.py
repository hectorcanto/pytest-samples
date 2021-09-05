

class SystemUnderTest:

    def __init__(self):
        pass

    @staticmethod
    def function(self, value):
        if value is None:
            return None
        if not isinstance(value, (int, float)):
            raise TypeError("Expected numeric")
        return 2 * value
