from . import abst
from .. import exceptions


class FnCoreOp(abst._OpBase):
    def __init__(self):
        super(FnCoreOp, self).__init__()

    @classmethod
    def type(cls):
        return cls.__name__

    def needs(self):
        raise exceptions.FnErrNotImplementedError(self, "needs")

    def params(self):
        raise exceptions.FnErrNotImplementedError(self, "params")

    def packetable(self):
        raise exceptions.FnErrNotImplementedError(self, "packetable")

    def operate(self, params, packetArray):
        raise exceptions.FnErrNotImplementedError(self, "operate")
