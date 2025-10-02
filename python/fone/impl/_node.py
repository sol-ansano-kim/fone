import uuid
from .. import exceptions


class _FoneNodeImpl(object):
    def __init__(self, op, node):
        super(_FoneNodeImpl, self).__init__()
        self.__id = uuid.uuid4()
        self.__op = op
        self.__node = node
        self.__inputs = [None] * self.__op.requiredInputs()
        self.__params = {}
        self.__outputs = set()
        for k, v in self.__op.params().items():
            self.__params[k] = v.copy()

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

    def paramNames(self):
        return sorted(self.__params.keys())

    def getParam(self, name):
        p = self.__params.get(name, None)
        if p is None:
            return None

        return p.copy()

    def getParamValue(self, name):
        return self.__params[name].get()

    def setParamValue(self, name, value):
        self.__params[name].set(value)

    def requiredInputs(self):
        return self.__op.requiredInputs()

    def generateOutput(self):
        return self.__op.generateOutput()

    def inputs(self):
        return self.__inputs[:]

    def outputs(self):
        return list(self.__outputs)

    def _connectOutput(self, nodeImpl):
        if nodeImpl in self.__outputs:
            return False

        if not self.__op.generateOutput():
            return False

        self.__outputs.add(nodeImpl)

        return True

    def _disconnectOutput(self, nodeImpl):
        if not nodeImpl in self.__outputs:
            return False

        self.__outputs.remove(nodeImpl)

        return True

    def connectInput(self, index, nodeImpl):
        if index >= self.__op.requiredInputs():
            raise exceptions.FoneIndexError(index, self.__op.requiredInputs())

        if not nodeImpl.generateOutput():
            return False

        _org = None
        if self.__inputs[index] is not None:
            _org = self.__inputs[index]

        self.__inputs[index] = nodeImpl
        self.__inputs[index]._connectOutput(self)

        if _org is not None and _org not in self.__inputs:
            _org._disconnectOutput(self)

        return True

    def disconnectInput(self, index):
        if index >= self.__op.requiredInputs():
            raise exceptions.FoneIndexError(index, self.__op.requiredInputs())

        if self.__inputs[index] is None:
            return False

        _org = self.__inputs[index]
        self.__inputs[index] = None

        if _org is not None and _org not in self.__inputs:
            _org._disconnectOutput(self)

        return True

    def disconnectAllInputs(self):
        for i in range(self.__op.requiredInputs()):
            self.disconnectInput(i)

        return True
