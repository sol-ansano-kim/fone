from . import abst
from . import node
from ..core import packet
from .. import exceptions


class FoneGraphScene(abst._GraphSceneBase):
    def __init__(self, scene):
        super(FoneGraphScene, self).__init__(scene)
        self.__scene = scene
        self.__graph_nodes = {}

    def __track_nodes(self):
        new_nodes = {}

        for sn in self.__scene.nodes():
            n = self.__graph_nodes.get(sn.__hash__(), None)
            if n is None:
                n = node.FoneGraphNode(sn)

            new_nodes[sn.__hash__()] = n

        self.__graph_nodes = new_nodes

    def __input_hashes(self, node):
        hashes = set()

        currents = [node]
        while (currents):
            nexts = []

            for cur in currents:
                if cur.__hash__() not in hashes:
                    hashes.add(cur.__hash__())
                    nexts.extend([x for x in cur.inputs() if x is not None])

            currents = nexts

        return hashes

    def __input_network(self, nodes):
        cache = set()
        eval_nodes = []

        currents = nodes[:]
        while (currents):
            nexts = []

            for cur in currents:
                if cur not in cache:
                    eval_nodes.append(cur)
                    cache.add(cur)
                    nexts.extend([x for x in cur.inputs() if x is not None])

            currents = nexts

        return [self.__graph_nodes[x.__hash__()] for x in reversed(eval_nodes)]

    def __evaluate(self, nodes, force=False):
        self.__track_nodes()

        waiting = self.__input_network(nodes)
        dirty_hashes = set([x.node().__hash__() for x in waiting if x.isDirty()])
        evaled = set()

        def _isDirty(n):
            if n.__hash__() in evaled:
                return False

            return len(self.__input_hashes(n).intersection(dirty_hashes)) > 0

        latest_count = None
        while (waiting):
            if len(waiting) == latest_count:
                raise exceptions.FoneGraphEvaluationError("Failed to evaludate the scene graph")

            latest_count = len(waiting)

            pending = []
            for _ in range(latest_count):
                gn = waiting.pop(0)

                if gn.node().__hash__() in evaled:
                    continue

                if not force and not _isDirty(gn.node()):
                    continue

                ready = True
                packets = []
                for inn in gn.node().inputs():
                    if inn is not None and _isDirty(inn):
                        ready = False
                        break

                    if inn is None:
                        packets.append(packet.FonePacket())
                    else:
                        packets.append(self.__graph_nodes[inn.__hash__()].packet())

                if not ready:
                    pending.append(gn)
                    continue

                gn.evaluate(packet.FonePacketArray(packets), force=True)
                evaled.add(gn.node().__hash__())

            waiting = pending + waiting

    def packet(self, node):
        if node.__hash__() not in self.__graph_nodes:
            self.__track_nodes()

        gn = self.__graph_nodes.get(node.__hash__())
        if gn is None:
            return None

        self.__evaluate([node])

        return gn.packet()
