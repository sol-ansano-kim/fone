from . import abst
from . import op
from ..impl import _opManager


class OFnOpManager(abst._OpManagerBase):
    __INSTANCE = None

    def __new__(self):
        if OFnOpManager.__INSTANCE is None:
            OFnOpManager.__INSTANCE = super(OFnOpManager, self).__new__(self)
            OFnOpManager.__INSTANCE.__initialize()

        return OFnOpManager.__INSTANCE

    def __init__(self):
        super(OFnOpManager, self).__init__()

    def __initialize(self):
        self.__impl = _opManager._OFnOpManagerImpl(op.OFnOp)

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


manager = OFnOpManager()
