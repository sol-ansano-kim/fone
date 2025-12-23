from . import abst
from . import node
from ..core import packet
from .. import exceptions


class FoneGraphScene(abst._GraphSceneBase):
    def __init__(self, scene):
        super(FoneGraphScene, self).__init__(scene)
        self.__scene = scene
        self.__graph_nodes = {}

    def __scratch_node(self):
        new_nodes = {}

        for sn in self.__scene.nodes():
            n = new_nodes.get(sn.__hash__(), None)
            if n is None:
                n = node.FoneGraphNode(sn)

            new_nodes[sn.__hash__()] = n

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

    def __evaluate(self, force=False):
        waiting = self.__schedule()

        latest_count = None
        while (waiting):
            if len(waiting) == latest_count:
                raise exceptions.FoneGraphEvaluationError("Failed to evaludate the scene graph")

            latest_count = len(waiting)

            pending = []
            for _ in range(latest_count):
                gn = waiting.pop(0)

                if not gn.isDirty():
                    continue

                ready = True
                packets = []
                for inn in gn.node().inputs():
                    if inn is not None and self.__graph_nodes[inn.__hash__()].isDirty():
                        ready = False
                        break

                    if inn is None:
                        packets.append(packet.FonePacket())
                    else:
                        packets.append(self.__graph_nodes[inn.__hash__()].packet())

                if not ready:
                    pending.append(gn)
                    continue

                gn.evaluate(packet.FonePacketArray(packets))

            waiting = pending + waiting

    def packet(self, node):
        if node.__hash__() not in self.__graph_nodes:
            self.__scratch_node()

        gn = self.__graph_nodes.get(node.__hash__())
        if gn is None:
            return None

        self.__evaluate(force=False)

        return gn.packet()
