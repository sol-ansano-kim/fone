from ..exceptions import FnErrNotImplementedError


class _NodeBase(object):
    def __init__(self):
        super(_NodeBase, self).__init__()

    def __hash__(self):
        raise FnErrNotImplementedError(self, "__hash__")

    def __eq__(self, other):
        raise FnErrNotImplementedError(self, "__eq__")

    def __neq__(self, other):
        raise FnErrNotImplementedError(self, "__neq__")

    def type(self):
        raise FnErrNotImplementedError(self, "type")

    def name(self):
        raise FnErrNotImplementedError(self, "name")

    def rename(self, newName):
        raise FnErrNotImplementedError(self, "rename")

    def paramNames(self):
        raise FnErrNotImplementedError(self, "paramNames")

    def getParam(self, name):
        raise FnErrNotImplementedError(self, "getParam")

    def getParamValue(self, name, default=None):
        raise FnErrNotImplementedError(self, "getParamValue")

    def setParamValue(self, name, value):
        raise FnErrNotImplementedError(self, "setParamValue")

    def needs(self):
        raise FnErrNotImplementedError(self, "needs")

    def packetable(self):
        raise FnErrNotImplementedError(self, "packetable")

    def inputs(self):
        raise FnErrNotImplementedError(self, "inputs")

    def outputs(self):
        raise FnErrNotImplementedError(self, "outputs")

    def connect(self, src, index=0):
        raise FnErrNotImplementedError(self, "connect")

    def disconnect(self, index=0):
        raise FnErrNotImplementedError(self, "disconnect")

    def disconnectAll(self):
        raise FnErrNotImplementedError(self, "disconnectAll")

    def operate(self, packetArray):
        raise FnErrNotImplementedError(self, "operate")


class _SceneBase(object):
    def __init__(self):
        super(_SceneBase, self).__init__()

    def createNode(self, type, name=None):
        raise FnErrNotImplementedError(self, "createNode")

    def deleteNode(self, node):
        raise FnErrNotImplementedError(self, "deleteNode")

    def nodes(self):
        raise FnErrNotImplementedError(self, "nodes")

    def getUniqueName(self, name):
        raise FnErrNotImplementedError(self, "getUniqueName")

    def read(self, filepath):
        raise FnErrNotImplementedError(self, "read")

    def write(self, filepath):
        raise FnErrNotImplementedError(self, "write")

    def clear(self):
        raise FnErrNotImplementedError(self, "clear")


class _OpBase(object):
    def __init__(self):
        super(_OpBase, self).__init__()

    @classmethod
    def type(cls):
        raise FnErrNotImplementedError(cls, "type")

    def needs(self):
        raise FnErrNotImplementedError(self, "needs")

    def params(self):
        raise FnErrNotImplementedError(self, "params")

    def packetable(self):
        raise FnErrNotImplementedError(self, "packetable")

    def operate(self, params, packetArray):
        raise FnErrNotImplementedError(self, "operate")


class _OpManagerBase(object):
    def __init__(self):
        super(_OpManagerBase, self).__init__()

    def reloadPlugins(self):
        raise FnErrNotImplementedError(self, "reloadPlugins")

    def listOps(self):
        raise FnErrNotImplementedError(self, "listOps")

    def getOp(self, opName):
        raise FnErrNotImplementedError(self, "getOp")

    def registerOp(self, op):
        raise FnErrNotImplementedError(self, "registerOp")

    def deregisterOp(self, op):
        raise FnErrNotImplementedError(self, "deregisterOp")


class _PacketBase(object):
    def __init__(self):
        super(_PacketBase, self).__init__()

    def copy(self):
        raise FnErrNotImplementedError(self, "copy")

    def metadata(self):
        raise FnErrNotImplementedError(self, "metadata")

    def data(self):
        raise FnErrNotImplementedError(self, "data")


class _PacketArrayBase(object):
    def __init__(self):
        super(_PacketArrayBase, self).__init__()

    def count(self):
        raise FnErrNotImplementedError(self, "count")

    def packet(self, index):
        raise FnErrNotImplementedError(self, "packet")


class _ParamBase(object):
    def __init__(self):
        super(_ParamBase, self).__init__()

    def default(self):
        raise FnErrNotImplementedError(self, "default")

    def get(self):
        raise FnErrNotImplementedError(self, "get")

    def set(self, value):
        raise FnErrNotImplementedError(self, "set")

    def type(self):
        raise FnErrNotImplementedError(self, "type")

    def isValid(self, value):
        raise FnErrNotImplementedError(self, "isValid")

    def copy(self):
        raise FnErrNotImplementedError(self, "copy")
