class FoneInvalidArgumentError(Exception):
    def __init__(self, expected, given):
        super(FoneInvalidArgumentError, self).__init__(f"Invalid argument - expected type '{expected.__name__}', but received '{type(given).__name__}'")


class FoneNotImplementedError(Exception):
    def __init__(self, instance, name):
        super(FoneNotImplementedError, self).__init__(f"'{instance.__class__.__name__}.{name}' is not implemented yet")
