from . import abst
from .node import FoneNode
from .opManager import manager


class FoneScene(abst._SceneBase):
    def __init__(self):
        super(FoneScene, self).__init__()
        self.__nodes = []

    def createNode(self, type, name=None):
        op = manager.getOp(type)
        if op is None:
            return None

        node = FoneNode(self, op, name=name)
        self.__nodes[node.__hash__()] = node

        return node

    def deleteNode(self, node):
        if node.__hash__() not in self.__nodes:
            return False

        self.__nodes.pop(node.__hash__())

        del node

    def nodes(self):
        return [x for x in self.__nodes.values()]

    def getUniqueName(self, name):
        index = 0

        while (True):
            nname = f"{name}{index}" if index > 0 else name

            used = False
            for n in self.__nodes.values():
                if n.name() == nname:
                    used = True
                    break

            if not used:
                return nname

    def read(self, filepath):
        pass

    def write(self, filepath):
        pass

    def clear(self):
        pass
