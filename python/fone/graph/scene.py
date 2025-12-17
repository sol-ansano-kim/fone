from . import abst
from . import node


class FoneGraphScene(abst._GraphSceneBase):
    def __init__(self, scene):
        super(FoneGraphScene, self).__init__()
        self.__scene = scene
        self.__graph_nodes = {}

    def __scratch_node(self):
        new_nodes = {}

        for node in self.__scene.nodes():
            n = new_nodes.get(node.__hash__(), None)
            if n is None:
                n = node.FoneGraphNode(node)

            new_nodes[node.__hash__()] = n

        self.__graph_nodes = new_nodes

    def __schedule(self):
        cache = set()

        currents = []
        for node in self.__scene.nodes():
            if not node.packetable():
                currents.append(node)

        eval_nodes = []
        while (currents):
            nexts = []

            for cur in currents:
                if cur not in cache:
                    eval_nodes.append(cur)
                    cache.add(cur)
                    nexts.extend([x for x in cur.inputs() if x is not None])

            currents = nexts

        return [self.__graph_nodes[x.__hash__()] for x in reversed(eval_nodes)]

    def evaluate(self, force=False):
        schedule = self.__schedule()

    def packet(self, node):
        if node.__hash__() not in self.__graph_nodes:
            self.__scratch_node()

        gn = self.__graph_nodes.get(node.__hash__())
        if gn is None:
            return None

        self.evaluate(force=False)

        return gn.packet()
