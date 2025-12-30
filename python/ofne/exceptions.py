class OFnInvalidArgumentError(Exception):
    def __init__(self, expected, given):
        super(OFnInvalidArgumentError, self).__init__(f"Invalid argument - expected type '{expected.__name__}', but received '{type(given).__name__}'")


class OFnNotImplementedError(Exception):
    def __init__(self, instance, name):
        import inspect
        cname = instance.__name__ if inspect.isclass(instance) else instance.__class__.__name__
        super(OFnNotImplementedError, self).__init__(f"'{cname}.{name}' is not implemented yet")


class OFnIndexError(Exception):
    def __init__(self, index, total):
        super(OFnIndexError, self).__init__(f"list index out of range : {index}/{total}")


class OFnInvalidParamValueError(Exception):
    def __init__(self, instance, value):
        super(OFnInvalidParamValueError, self).__init__(f"Invalid value '{value}' given for '{instance.__class__.__name__}'")


class OFnGraphEvaluationError(Exception):
    pass
