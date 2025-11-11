class _FoneSceneImpl(object):
    def __init__(self, nodeClass, opManager):
        super(_FoneSceneImpl, self).__init__()
        self.__node_class = nodeClass
        self.__op_manager = opManager
        self.__nodes = {}

    def createNode(self, type, name=None):
        op = self.__op_manager.getOp(type)
        if op is None:
            return None

        node = self.__node_class(self, op, name=name)
        self.__nodes[node.__hash__()] = node

        return node

    def deleteNode(self, node):
        if node.__hash__() not in self.__nodes:
            return False

        self.__nodes.pop(node.__hash__())

        del node

        return True

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

            index += 1

    def read(self, filepath):
        pass

    def write(self, filepath):
        pass

    def clear(self):
        pass
