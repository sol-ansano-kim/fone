from . import abst
from .. import exceptions


FnCoreParamTypeBool = 0
FnCoreParamTypeInt = 1
FnCoreParamTypeFloat = 2
FnCoreParamTypeStr = 3


class FnCoreParamBase(abst._ParamBase):
    def __init__(self, default):
        super(FnCoreParamBase, self).__init__()
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
            raise exceptions.FnErrInvalidParamValueError(self, value)

        self.__value = value

    def type(self):
        raise exceptions.FnErrNotImplementedError(self, "type")

    def isValid(self, value):
        raise exceptions.FnErrNotImplementedError(self, "isValid")

    def copy(self):
        raise exceptions.FnErrNotImplementedError(self, "copy")


class FnCoreParamBool(FnCoreParamBase):
    def __init__(self, default=False):
        super(FnCoreParamBool, self).__init__(default)

    def type(self):
        return FnCoreParamTypeBool

    def isValid(self, value):
        return isinstance(value, bool)

    def copy(self):
        n = FnCoreParamBool(self.default())
        n.set(self.get())

        return n


class FnCoreParamStr(FnCoreParamBase):
    def __init__(self, default="", valueList=None, enforceValueList=False):
        self.__value_list = list(valueList) if isinstance(valueList, (list, tuple, set)) else []
        self.__enforce_value_list = enforceValueList if self.__value_list else False

        super(FnCoreParamStr, self).__init__(default)

    def type(self):
        return FnCoreParamTypeStr

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
        n = FnCoreParamStr(default=self.default(), valueList=self.__value_list, enforceValueList=self.__enforce_value_list)
        n.set(self.get())

        return n


class FoneNumericParam(FnCoreParamBase):
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


class FnCoreParamInt(FoneNumericParam):
    def __init__(self, default=0, min=None, max=None):
        super(FnCoreParamInt, self).__init__(default=default, min=min, max=max)

    def type(self):
        return FnCoreParamTypeInt

    def isValid(self, value):
        if not isinstance(value, int):
            return False

        if isinstance(value, bool):
            return False

        return super(FnCoreParamInt, self).isValid(value)


class FnCoreParamFloat(FoneNumericParam):
    def __init__(self, default=0.0, min=None, max=None):
        super(FnCoreParamFloat, self).__init__(default=default, min=min, max=max)

    def type(self):
        return FnCoreParamTypeFloat

    def isValid(self, value):
        if not isinstance(value, float):
            return False

        return super(FnCoreParamFloat, self).isValid(value)


class FnCoreParams(object):
    def __init__(self, paramDict):
        super(FnCoreParams).__init__()
        self.__params = {}
        for key, param in paramDict.items():
            self.__params[key] = param.copy()

    def copy(self):
        nparm = {}
        for key, param in self.__params.items():
            nparm[key] = param.copy()

        return FnCoreParams(nparm)

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