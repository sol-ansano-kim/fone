from .. import exceptions
from ..impl import _node


class FoneNode(object):
    def __init__(self, op):
        super(FoneNode, self).__init__()
        self.__impl = _node._FoneNodeImpl(op, self)

    def type(self):
        return self.__impl.type()

    def requiredInputs(self):
        return self.__impl.requiredInputs()

    def inputs(self):
        return self.__impl.inputs()

    def outputs(self):
        return self.__impl.outputs()
