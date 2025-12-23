class FoneInvalidArgumentError(Exception):
    def __init__(self, expected, given):
        super(FoneInvalidArgumentError, self).__init__(f"Invalid argument - expected type '{expected.__name__}', but received '{type(given).__name__}'")


class FoneNotImplementedError(Exception):
    def __init__(self, instance, name):
        import inspect
        cname = instance.__name__ if inspect.isclass(instance) else instance.__class__.__name__
        super(FoneNotImplementedError, self).__init__(f"'{cname}.{name}' is not implemented yet")


class FoneIndexError(Exception):
    def __init__(self, index, total):
        super(FoneIndexError, self).__init__(f"list index out of range : {index}/{total}")


class FoneInvalidParamValueError(Exception):
    def __init__(self, instance, value):
        super(FoneInvalidParamValueError, self).__init__(f"Invalid value '{value}' given for '{instance.__class__.__name__}'")


class FoneGraphEvaluationError(Exception):
    pass
