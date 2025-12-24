from . import abst
from . import op
from ..impl import _opManager


class FnCoreOpManager(abst._OpManagerBase):
    __INSTANCE = None

    def __new__(self):
        if FnCoreOpManager.__INSTANCE is None:
            FnCoreOpManager.__INSTANCE = super(FnCoreOpManager, self).__new__(self)
            FnCoreOpManager.__INSTANCE.__initialize()

        return FnCoreOpManager.__INSTANCE

    def __init__(self):
        super(FnCoreOpManager, self).__init__()

    def __initialize(self):
        self.__impl = _opManager._FnCoreOpManagerImpl(op.FnCoreOp)

    def reloadPlugins(self):
        self.__impl.reloadPlugins()

    def listOps(self):
        return self.__impl.listOps()

    def getOp(self, opName):
        return self.__impl.getOp(opName)

    def registerOp(self, op):
        return self.__impl.registerOp(op)

    def deregisterOp(self, op):
        return self.__impl.deregisterOp(op)


manager = FnCoreOpManager()
