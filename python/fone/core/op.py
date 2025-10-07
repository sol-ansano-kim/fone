from .. import exceptions


class FoneOp(object):
    def __init__(self):
        super(FoneOp, self).__init__()

    def type(self):
        raise exceptions.FoneNotImplementedError(self, "type")

    def needs(self):
        raise exceptions.FoneNotImplementedError(self, "needs")

    def params(self):
        raise exceptions.FoneNotImplementedError(self, "params")

    def packetable(self):
        raise exceptions.FoneNotImplementedError(self, "packetable")
