class FoneGraphNode(object):
    def __init__(self, node):
        super(FoneGraphNode, self).__init__()
        self.__node = node

    def __eq__(self, other):
        return isinstance(other, FoneGraphNode) and other.node() == self.node()

    def __neq__(self, other):
        return not self.__eq__(other)

    def node(self):
        return self.__node

    def inputs(self):
        inpts = []
        for node in self.__node.inputs():
            if node is not None:
                node = FoneGraphNode(node)

            inpts.append(node)

        return inpts
