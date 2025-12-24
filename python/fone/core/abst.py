from ..exceptions import FoneNotImplementedError


class _NodeBase(object):
    def __init__(self):
        super(_NodeBase, self).__init__()

    def __hash__(self):
        raise FoneNotImplementedError(self, "__hash__")

    def __eq__(self, other):
        raise FoneNotImplementedError(self, "__eq__")

    def __neq__(self, other):
        raise FoneNotImplementedError(self, "__neq__")

    def type(self):
        raise FoneNotImplementedError(self, "type")

    def name(self):
        raise FoneNotImplementedError(self, "name")

    def rename(self, newName):
        raise FoneNotImplementedError(self, "rename")

    def paramNames(self):
        raise FoneNotImplementedError(self, "paramNames")

    def getParam(self, name):
        raise FoneNotImplementedError(self, "getParam")

    def getParamValue(self, name, default=None):
        raise FoneNotImplementedError(self, "getParamValue")

    def setParamValue(self, name, value):
        raise FoneNotImplementedError(self, "setParamValue")

    def needs(self):
        raise FoneNotImplementedError(self, "needs")

    def packetable(self):
        raise FoneNotImplementedError(self, "packetable")

    def inputs(self):
        raise FoneNotImplementedError(self, "inputs")

    def outputs(self):
        raise FoneNotImplementedError(self, "outputs")

    def connect(self, src, index=0):
        raise FoneNotImplementedError(self, "connect")

    def disconnect(self, index=0):
        raise FoneNotImplementedError(self, "disconnect")

    def disconnectAll(self):
        raise FoneNotImplementedError(self, "disconnectAll")

    def operate(self, packetArray):
        raise FoneNotImplementedError(self, "operate")


class _SceneBase(object):
    def __init__(self):
        super(_SceneBase, self).__init__()

    def createNode(self, type, name=None):
        raise FoneNotImplementedError(self, "createNode")

    def deleteNode(self, node):
        raise FoneNotImplementedError(self, "deleteNode")

    def nodes(self):
        raise FoneNotImplementedError(self, "nodes")

    def getUniqueName(self, name):
        raise FoneNotImplementedError(self, "getUniqueName")

    def read(self, filepath):
        raise FoneNotImplementedError(self, "read")

    def write(self, filepath):
        raise FoneNotImplementedError(self, "write")

    def clear(self):
        raise FoneNotImplementedError(self, "clear")


class _OpBase(object):
    def __init__(self):
        super(_OpBase, self).__init__()

    @classmethod
    def type(cls):
        raise FoneNotImplementedError(cls, "type")

    def needs(self):
        raise FoneNotImplementedError(self, "needs")

    def params(self):
        raise FoneNotImplementedError(self, "params")

    def packetable(self):
        raise FoneNotImplementedError(self, "packetable")

    def operate(self, params, packetArray):
        raise FoneNotImplementedError(self, "operate")


class _OpManagerBase(object):
    def __init__(self):
        super(_OpManagerBase, self).__init__()

    def reloadPlugins(self):
        raise FoneNotImplementedError(self, "reloadPlugins")

    def listOps(self):
        raise FoneNotImplementedError(self, "listOps")

    def getOp(self, opName):
        raise FoneNotImplementedError(self, "getOp")

    def registerOp(self, op):
        raise FoneNotImplementedError(self, "registerOp")

    def deregisterOp(self, op):
        raise FoneNotImplementedError(self, "deregisterOp")


class _PacketBase(object):
    def __init__(self):
        super(_PacketBase, self).__init__()

    def copy(self):
        raise FoneNotImplementedError(self, "copy")

    def metadata(self):
        raise FoneNotImplementedError(self, "metadata")

    def data(self):
        raise FoneNotImplementedError(self, "data")


class _PacketArrayBase(object):
    def __init__(self):
        super(_PacketArrayBase, self).__init__()

    def count(self):
        raise FoneNotImplementedError(self, "count")

    def packet(self, index):
        raise FoneNotImplementedError(self, "packet")


class _ParamBase(object):
    def __init__(self):
        super(_ParamBase, self).__init__()

    def default(self):
        raise FoneNotImplementedError(self, "default")

    def get(self):
        raise FoneNotImplementedError(self, "get")

    def set(self, value):
        raise FoneNotImplementedError(self, "set")

    def type(self):
        raise FoneNotImplementedError(self, "type")

    def isValid(self, value):
        raise FoneNotImplementedError(self, "isValid")

    def copy(self):
        raise FoneNotImplementedError(self, "copy")
