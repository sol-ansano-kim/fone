from .. import exceptions


FoneParamTypeBool = 0
FoneParamTypeInt = 1
FoneParamTypeFloat = 2
FoneParamTypeStr = 3


class FoneParamBase(object):
    def __init__(self, default):
        super(FoneParamBase, self).__init__()
        self.__value = None
        self.__default = None

        self.set(default)
        self.__default = self.__value

    def default(self):
        return self.__default

    def get(self):
        return self.__value

    def set(self, value):
        if not self.isValid(value):
            raise exceptions.FoneInvalidParamValueError(self, value)

        self.__value = value

    def type(self):
        raise exceptions.FoneNotImplementedError(self, "type")

    def isValid(self, value):
        raise exceptions.FoneNotImplementedError(self, "isValid")

    def copy(self):
        raise exceptions.FoneNotImplementedError(self, "copy")


class FoneParamBool(FoneParamBase):
    def __init__(self, default=False):
        super(FoneParamBool, self).__init__(default)

    def type(self):
        return FoneParamTypeBool

    def isValid(self, value):
        return isinstance(value, bool)

    def copy(self):
        n = FoneParamBool(self.default())
        n.set(self.get())

        return n


class FoneParamStr(FoneParamBase):
    def __init__(self, default="", valueList=None, enforceValueList=False):
        self.__value_list = list(valueList) if isinstance(valueList, (list, tuple, set)) else []
        self.__enforce_value_list = enforceValueList if self.__value_list else False

        super(FoneParamStr, self).__init__(default)

    def type(self):
        return FoneParamTypeStr

    def enforceValueList(self):
        return self.__enforce_value_list

    def valueList(self):
        return self.__value_list[:]

    def isValid(self, value):
        if not isinstance(value, str):
            return False

        if self.__enforce_value_list and value not in self.__value_list:
            return False

        return True

    def copy(self):
        n = FoneParamStr(default=self.default(), valueList=self.__value_list, enforceValueList=self.__enforce_value_list)
        n.set(self.get())

        return n


class FoneNumericParam(FoneParamBase):
    def __init__(self, default=None, min=None, max=None):
        self.__min = min
        self.__max = max

        super(FoneNumericParam, self).__init__(default)

    def min(self):
        return self.__min

    def max(self):
        return self.__max

    def isValid(self, value):
        if self.__min is not None and value < self.__min:
            return False

        if self.__max is not None and value > self.__max:
            return False

        return True

    def copy(self):
        n = self.__class__(default=self.default(), min=self.__min, max=self.__max)
        n.set(self.get())

        return n


class FoneParamInt(FoneNumericParam):
    def __init__(self, default=0, min=None, max=None):
        super(FoneParamInt, self).__init__(default=default, min=min, max=max)

    def type(self):
        return FoneParamTypeInt

    def isValid(self, value):
        if not isinstance(value, int):
            return False

        if isinstance(value, bool):
            return False

        return super(FoneParamInt, self).isValid(value)


class FoneParamFloat(FoneNumericParam):
    def __init__(self, default=0.0, min=None, max=None):
        super(FoneParamFloat, self).__init__(default=default, min=min, max=max)

    def type(self):
        return FoneParamTypeFloat

    def isValid(self, value):
        if not isinstance(value, float):
            return False

        return super(FoneParamFloat, self).isValid(value)


class FoneParams(object):
    def __init__(self, param_dict):
        super(FoneParams).__init__()
        self.__params = {}
        for key, param in param_dict.items():
            self.__params[key] = param.copy()

    def getParam(self, key):
        if key not in self.__params:
            return None

        return self.__params[key].copy()

    def get(self, key, default=None):
        if key not in self.__params:
            return default

        return self.__params[key].get()

    def set(self, key, value):
        if key not in self.__params:
            return False

        self.__params[key].set(value)
        return True

    def keys(self):
        return sorted(self.__params.keys())