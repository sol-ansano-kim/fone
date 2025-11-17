from ..exceptions import FoneNotImplementedError


class _GraphNodeBase(object):
    def __init__(self):
        super(_GraphNodeBase, self).__init__()

    def isDirty(self):
        raise FoneNotImplementedError(self, "isDirty")

    def evaluate(self):
        raise FoneNotImplementedError(self, "evaluate")

    def packet(self):
        raise FoneNotImplementedError(self, "packet")


class _GraphSceneBase(object):
    def __init__(self, scene):
        super(_GraphSceneBase, self).__init__()

    def evaluate(self):
        raise FoneNotImplementedError(self, "evaluate")

    def packet(self, node):
        raise FoneNotImplementedError(self, "packet")
