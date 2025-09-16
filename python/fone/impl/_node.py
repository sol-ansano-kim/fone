import uuid
from .. import exceptions


class _FoneNodeImpl(object):
    def __init__(self, op, node):
        super(_FoneNodeImpl, self).__init__()
        self.__id = uuid.uuid4()
        self.__op = op
        self.__node = node
        self.__inputs = [None] * self.__op.requiredInputs()
        self.__outputs = set()

    def __hash__(self):
        return self.__id.int

    def id(self):
        return self.__id

    def __eq__(self, other):
        return isinstance(other, _FoneNodeImpl) and other.id() == self.__id

    def __neq__(self, other):
        return not self.__eq__(other)

    def node(self):
        return self.__node

    def type(self):
        return self.__op.type()

    def requiredInputs(self):
        return self.__op.requiredInputs()

    def connectOutput(self, nodeImpl):
        if nodeImpl in self.__outputs:
            return False

        self.__outputs.add(nodeImpl)

        return True

    def disconnectOutput(self, nodeImpl):
        if not nodeImpl in self.__outputs:
            return False

        self.__outputs.remove(nodeImpl)

        return True

    def connectInput(self, index, nodeImpl):
        if index >= len(self.__op.requiredInputs()):
            raise exceptions.FoneIndexError(index, self.__op.requiredInputs())

        if self.__inputs[index] is not None:
            self.__inputs[index].disconnectOutput(self)

        self.__inputs[index] = nodeImpl
        self.__inputs[index].connectOutput(self)

        return True

    def disconnectInput(self, index):
        if index >= len(self.__op.requiredInputs()):
            raise exceptions.FoneIndexError(index, self.__op.requiredInputs())

        if self.__inputs[index] is None:
            return False

        self.__inputs[index].disconnectOutput(self)
        self.__inputs[index] = None

        return True

    def disconnectAllInputs(self):
        for i in range(self.__op.requiredInputs()):
            self.disconnectInput(i)

        return True
