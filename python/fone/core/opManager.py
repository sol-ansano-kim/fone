from . import abst
from . import op
from ..impl import _opManager


class FoneOpManager(abst._OpManagerBase):
    __INSTANCE = None

    def __new__(self):
        if FoneOpManager.__INSTANCE is None:
            FoneOpManager.__INSTANCE = super(FoneOpManager, self).__new__(self)
            FoneOpManager.__INSTANCE.__initialize()

        return FoneOpManager.__INSTANCE

    def __init__(self):
        super(FoneOpManager, self).__init__()

    def __initialize(self):
        self.__impl = _opManager._FoneOpManagerImpl(op.FoneOp)

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


manager = FoneOpManager()
