from .. import exceptions


class FoneOp(object):
    def __init__(self):
        super(FoneOp, self).__init__()

    def type(self):
        raise exceptions.FoneNotImplementedError(self, "type")

    def requiredInputs(self):
        raise exceptions.FoneNotImplementedError(self, "requiredInputs")

    def params(self):
        raise exceptions.FoneNotImplementedError(self, "params")
