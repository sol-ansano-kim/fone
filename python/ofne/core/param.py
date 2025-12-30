from . import abst
from .. import exceptions


ParamTypeBool = 0
ParamTypeInt = 1
ParamTypeFloat = 2
ParamTypeStr = 3


class OFnParamBase(abst._ParamBase):
    def __init__(self, default):
        super(OFnParamBase, self).__init__()
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
            raise exceptions.OFnInvalidParamValueError(self, value)

        self.__value = value

    def type(self):
        raise exceptions.OFnNotImplementedError(self, "type")

    def isValid(self, value):
        raise exceptions.OFnNotImplementedError(self, "isValid")

    def copy(self):
        raise exceptions.OFnNotImplementedError(self, "copy")


class OFnParamBool(OFnParamBase):
    def __init__(self, default=False):
        super(OFnParamBool, self).__init__(default)

    def type(self):
        return ParamTypeBool

    def isValid(self, value):
        return isinstance(value, bool)

    def copy(self):
        n = OFnParamBool(self.default())
        n.set(self.get())

        return n


class OFnParamStr(OFnParamBase):
    def __init__(self, default="", valueList=None, enforceValueList=False):
        self.__value_list = list(valueList) if isinstance(valueList, (list, tuple, set)) else []
        self.__enforce_value_list = enforceValueList if self.__value_list else False

        super(OFnParamStr, self).__init__(default)

    def type(self):
        return ParamTypeStr

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
        n = OFnParamStr(default=self.default(), valueList=self.__value_list, enforceValueList=self.__enforce_value_list)
        n.set(self.get())

        return n


class OFnNumericParam(OFnParamBase):
    def __init__(self, default=None, min=None, max=None):
        self.__min = min
        self.__max = max

        super(OFnNumericParam, self).__init__(default)

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


class OFnParamInt(OFnNumericParam):
    def __init__(self, default=0, min=None, max=None):
        super(OFnParamInt, self).__init__(default=default, min=min, max=max)

    def type(self):
        return ParamTypeInt

    def isValid(self, value):
        if not isinstance(value, int):
            return False

        if isinstance(value, bool):
            return False

        return super(OFnParamInt, self).isValid(value)


class OFnParamFloat(OFnNumericParam):
    def __init__(self, default=0.0, min=None, max=None):
        super(OFnParamFloat, self).__init__(default=default, min=min, max=max)

    def type(self):
        return ParamTypeFloat

    def isValid(self, value):
        if not isinstance(value, float):
            return False

        return super(OFnParamFloat, self).isValid(value)


class OFnParams(object):
    def __init__(self, paramDict):
        super(OFnParams).__init__()
        self.__params = {}
        for key, param in paramDict.items():
            self.__params[key] = param.copy()

    def copy(self):
        nparm = {}
        for key, param in self.__params.items():
            nparm[key] = param.copy()

        return OFnParams(nparm)

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