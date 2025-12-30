from ..exceptions import FnErrNotImplementedError


class _GraphNodeBase(object):
    def __init__(self, node):
        super(_GraphNodeBase, self).__init__()

    def node(self):
        raise FnErrNotImplementedError(self, "node")

    def dirty(self):
        raise FnErrNotImplementedError(self, "dirty")

    def isDirty(self):
        raise FnErrNotImplementedError(self, "isDirty")

    def evaluate(self, packetArray):
        raise FnErrNotImplementedError(self, "evaluate")

    def packet(self):
        raise FnErrNotImplementedError(self, "packet")


class _GraphSceneBase(object):
    def __init__(self, scene):
        super(_GraphSceneBase, self).__init__()

    def evaluate(self, nodes, force=False):
        raise FnErrNotImplementedError(self, "evaluate")

    def packet(self, nodes):
        raise FnErrNotImplementedError(self, "packet")
