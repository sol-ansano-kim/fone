import unittest
import numpy as np


class GraphNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from fone.core import packet
        except:
            import sys
            import os
            sys.path.append((os.path.abspath(os.path.join(__file__, "../../python"))))
        finally:
            from fone.core import node as core_node
            from fone.core import scene as core_scene
            from fone.core import op
            from fone.core import opManager
            from fone.core import param
            from fone.core import packet
            from fone.graph import node as graph_node
            from fone.graph import scene as graph_scene
            from fone import exceptions
            cls.core_node = core_node
            cls.core_scene = core_scene
            cls.graph_node = graph_node
            cls.exceptions = exceptions
            cls.param = param
            cls.packet = packet
            cls.opManager = opManager
            opManager

            class PlusOp(op.FoneOp):
                def __init__(self):
                    super(PlusOp, self).__init__()

                def params(self):
                    return {
                        "num": cls.param.FoneParamFloat()
                    }

                def needs(self):
                    return 1

                def packetable(self):
                    return True

                def operate(self, params, packetArray):
                    GraphNode.count += 1
                    return GraphNode.packet.FonePacket(data=packetArray.packet(0).data() + params.get("num"))

            class MakeNums(op.FoneOp):
                def __init__(self):
                    super(MakeNums, self).__init__()

                def params(self):
                    return {
                        "count": cls.param.FoneParamInt(min=0),
                        "num": cls.param.FoneParamFloat()
                    }

                def needs(self):
                    return 0

                def packetable(self):
                    return True

                def operate(self, params, packetArray):
                    GraphNode.count += 1
                    return GraphNode.packet.FonePacket(data=np.array([params.get("num")] * params.get("count")))

            cls.PlusOp = PlusOp()
            cls.MakeNums = MakeNums()
            cls.scene = core_scene.FoneScene()
            cls.count = 0

            opManager.FoneOpManager().registerOp(cls.PlusOp)
            opManager.FoneOpManager().registerOp(cls.MakeNums)

    @classmethod
    def tearDownClass(cls):
        cls.opManager.FoneOpManager().deregisterOp(cls.PlusOp)
        cls.opManager.FoneOpManager().deregisterOp(cls.MakeNums)

    def test_creation(self):
        self.assertEqual(len(self.opManager.FoneOpManager().listOps()), 2)
        self.assertIsNotNone(self.opManager.FoneOpManager().getOp("PlusOp"))
        self.assertIsNotNone(self.opManager.FoneOpManager().getOp("MakeNums"))

        scn = self.core_scene.FoneScene()
        self.assertIsNotNone(scn.createNode("PlusOp"))
        self.assertIsNotNone(scn.createNode("MakeNums"))
