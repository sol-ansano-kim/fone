from fone.core import op


class MyOpB(op.FoneOp):
    def __init__(self):
        super(MyOpB, self).__init__()

    def needs(self):
        return 0

    def params(self):
        return {}

    def packetable(self):
        return False


class MyOpC(object):
    pass
