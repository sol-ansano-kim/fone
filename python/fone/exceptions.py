class FnErrInvalidArgumentError(Exception):
    def __init__(self, expected, given):
        super(FnErrInvalidArgumentError, self).__init__(f"Invalid argument - expected type '{expected.__name__}', but received '{type(given).__name__}'")


class FnErrNotImplementedError(Exception):
    def __init__(self, instance, name):
        import inspect
        cname = instance.__name__ if inspect.isclass(instance) else instance.__class__.__name__
        super(FnErrNotImplementedError, self).__init__(f"'{cname}.{name}' is not implemented yet")


class FnErrIndexError(Exception):
    def __init__(self, index, total):
        super(FnErrIndexError, self).__init__(f"list index out of range : {index}/{total}")


class FnErrInvalidParamValueError(Exception):
    def __init__(self, instance, value):
        super(FnErrInvalidParamValueError, self).__init__(f"Invalid value '{value}' given for '{instance.__class__.__name__}'")


class FnErrGraphEvaluationError(Exception):
    pass
