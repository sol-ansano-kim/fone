from .. import exceptions
from ..impl import _node


class FoneNode(object):
    def __init__(self, op):
        super(FoneNode, self).__init__()
        self.__impl = _node._FoneNodeImpl(op, self)

    def type(self):
        return self.__impl.type()

    def paramNames(self):
        return self.__impl.paramNames()

    def getParam(self, name):
        return self.__impl.getParam(name)

    def getParamValue(self, name):
        return self.__impl.getParamValue(name)

    def setParamValue(self, name, value):
        self.__impl.setParamValue(name, value)

    def needs(self):
        return self.__impl.needs()

    def packetable(self):
        return self.__impl.packetable()

    def inputs(self):
        inpts = []
        for i in self.__impl.inputs():
            if i is not None:
                i = i.node()
            inpts.append(i)

        return inpts

    def outputs(self):
        oupts = []
        for o in self.__impl.outputs():
            if o is not None:
                o = o.node()
            oupts.append(o)

        return oupts

    def connect(self, src, index=0):
        return self.__impl.connectInput(index, src.__impl)

    def disconnect(self, index=0):
        return self.__impl.disconnectInput(index)

    def disconnectAll(self):
        return self.__impl.disconnectAllInputs()
