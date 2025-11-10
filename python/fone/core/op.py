from . import abst
from .. import exceptions


class FoneOp(abst._OpBase):
    def __init__(self):
        super(FoneOp, self).__init__()

    @classmethod
    def type(cls):
        return cls.__name__

    def needs(self):
        raise exceptions.FoneNotImplementedError(self, "needs")

    def params(self):
        raise exceptions.FoneNotImplementedError(self, "params")

    def packetable(self):
        raise exceptions.FoneNotImplementedError(self, "packetable")

    def operate(self, params, packetArray):
        raise exceptions.FoneNotImplementedError(self, "operate")
