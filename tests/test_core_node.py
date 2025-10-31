import unittest
import numpy as np


class CoreNode(unittest.TestCase):
    @classmethod
    def setUp(cls):
        try:
            from fone.core import packet
        except:
            import sys
            import os
            sys.path.append((os.path.abspath(os.path.join(__file__, "../../python"))))
        finally:
            from fone.core import node
            from fone.core import op
            from fone.core import param
            from fone.core import packet
            from fone import exceptions
            cls.node = node
            cls.exceptions = exceptions
            cls.param = param
            cls.packet = packet

        class OneInputs(op.FoneOp):
            def __init__(self):
                super(OneInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def params(self):
                return {}

            def needs(self):
                return 1

            def packetable(self):
                return True

        class TwoInputs(op.FoneOp):
            def __init__(self):
                super(TwoInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def params(self):
                return {}

            def needs(self):
                return 2

            def packetable(self):
                return False

        class ZeroInputs(op.FoneOp):
            def __init__(self):
                super(ZeroInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def params(self):
                return {}

            def needs(self):
                return 0

            def packetable(self):
                return True

        class ParamTester(op.FoneOp):
            def __init__(self):
                super(ParamTester, self).__init__()

            def type(self):
                return self.__class__.__name__

            def params(self):
                return {
                    "int": cls.param.FoneParamInt(),
                    "bool": cls.param.FoneParamBool(),
                    "float": cls.param.FoneParamFloat(),
                    "str": cls.param.FoneParamStr(),
                }

            def needs(self):
                return 0

            def packetable(self):
                return True

        class PlusOp(op.FoneOp):
            def __init__(self):
                super(PlusOp, self).__init__()

            def type(self):
                return "Plus"

            def params(self):
                return {
                    "num": cls.param.FoneParamFloat()
                }

            def needs(self):
                return 1

            def packetable(self):
                return True

            def operate(self, params, packetArray):
                return CoreNode.packet.FonePacket(data=packetArray.packet(0).data() + params.get("num"))

        class MakeNums(op.FoneOp):
            def __init__(self):
                super(MakeNums, self).__init__()

            def type(self):
                return "Make"

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
                return CoreNode.packet.FonePacket(data=np.array([params.get("num")] * params.get("count")))

        cls.OneInputs = OneInputs
        cls.ZeroInputs = ZeroInputs
        cls.TwoInputs = TwoInputs
        cls.ParamTester = ParamTester
        cls.PlusOp = PlusOp
        cls.MakeNums = MakeNums

    def test_params(self):
        ptop = self.ParamTester()
        pt1 = self.node.FoneNode(ptop)
        self.assertEqual(sorted(pt1.paramNames()), ["bool", "float", "int", "str"])
        bp = pt1.getParam("bool")
        self.assertEqual(bp.get(), pt1.getParamValue("bool"))
        self.assertFalse(pt1.getParamValue("bool"))
        bp.set(True)
        self.assertTrue(bp.get())
        self.assertNotEqual(bp.get(), pt1.getParamValue("bool"))
        self.assertFalse(pt1.getParamValue("bool"))
        self.assertIsNone(pt1.getParam("Abc"))
        self.assertEqual(pt1.getParamValue("int"), 0)
        pt1.setParamValue("int", 1)
        self.assertEqual(pt1.getParamValue("int"), 1)
        ip = pt1.getParam("int")
        self.assertEqual(ip.get(), pt1.getParamValue("int"))
        pt1.setParamValue("int", 2)
        self.assertNotEqual(ip.get(), pt1.getParamValue("int"))
        ip.set(2)
        self.assertEqual(ip.get(), pt1.getParamValue("int"))

    def test_connection(self):
        i0 = self.node.FoneNode(self.ZeroInputs())
        i1 = self.node.FoneNode(self.OneInputs())

        self.assertTrue(i1.connect(i0))
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        inputs = i1.inputs()
        inputs.pop(0)
        self.assertTrue(len(inputs) == 0)
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(i1.inputs()[0], i0)
        self.assertEqual(len(i0.outputs()), 1)
        outputs = i0.outputs()
        outputs.pop(0)
        self.assertTrue(len(outputs) == 0)
        self.assertEqual(len(i0.outputs()), 1)
        self.assertEqual(i0.outputs()[0], i1)
        self.assertTrue(i1.connect(i0))
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(i1.inputs()[0], i0)
        self.assertEqual(len(i0.outputs()), 1)
        self.assertEqual(i0.outputs()[0], i1)

        self.assertTrue(i1.disconnect(0))
        self.assertEqual(len([x for x in i1.inputs() if x]), 0)
        self.assertEqual(len(i0.outputs()), 0)
        self.assertFalse(i1.disconnect(0))

        with self.assertRaises(self.exceptions.FoneIndexError):
            self.assertTrue(i1.connect(i0, 1))
        with self.assertRaises(self.exceptions.FoneIndexError):
            self.assertTrue(i1.disconnect(1))

        i2 = self.node.FoneNode(self.TwoInputs())
        self.assertTrue(i1.connect(i0, 0))
        self.assertFalse(i1.connect(i2, 0))
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(i1.inputs()[0], i0)

        i01 = self.node.FoneNode(self.ZeroInputs())
        i02 = self.node.FoneNode(self.ZeroInputs())
        i1 = self.node.FoneNode(self.OneInputs())
        i2 = self.node.FoneNode(self.TwoInputs())

        self.assertTrue(i1.connect(i01, 0))
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(len(i01.outputs()), 1)
        self.assertEqual(len(i02.outputs()), 0)
        self.assertTrue(i1.connect(i02, 0))
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(len(i01.outputs()), 0)
        self.assertEqual(len(i02.outputs()), 1)

        i2.connect(i02, 0)
        i2.connect(i1, 1)
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(len(i02.outputs()), 2)
        self.assertEqual(len(i1.outputs()), 1)

        i2.disconnectAll()
        self.assertEqual(len([x for x in i2.inputs() if x]), 0)
        self.assertEqual(len(i02.outputs()), 1)
        self.assertEqual(len(i1.outputs()), 0)
        i1.disconnectAll()
        self.assertEqual(len(i02.outputs()), 0)
        self.assertEqual(len([x for x in i1.inputs() if x]), 0)

    def test_operaion(self):
        op_plus = self.PlusOp()
        op_make = self.MakeNums()
        node_plus = self.node.FoneNode(op_plus)
        node_make = self.node.FoneNode(op_make)
        pck = node_make.operate(self.packet.FonePacketArray([]))
        self.assertIsNotNone(pck)
        self.assertEqual(len(pck.data()), 0)

        node_make.setParamValue("count", 2)
        pck2 = node_make.operate(self.packet.FonePacketArray([]))
        self.assertEqual(len(pck2.data()), 2)
        self.assertEqual(pck2.data()[0], pck2.data()[1])
        self.assertEqual(pck2.data()[0], 0)

        node_make.setParamValue("num", 1.0)
        node_make.setParamValue("count", 3)
        pck3 = node_make.operate(self.packet.FonePacketArray([]))
        self.assertEqual(len(pck3.data()), 3)
        self.assertEqual(pck3.data()[0], pck3.data()[1])
        self.assertEqual(pck3.data()[0], pck3.data()[2])
        self.assertEqual(pck3.data()[0], 1.0)

        ppck = node_plus.operate(self.packet.FonePacketArray([pck3]))
        self.assertEqual(len(ppck.data()), 3)
        self.assertEqual(ppck.data()[0], ppck.data()[1])
        self.assertEqual(ppck.data()[0], ppck.data()[2])
        self.assertEqual(ppck.data()[0], 1.0)

        node_plus.setParamValue("num", 3.5)
        ppck = node_plus.operate(self.packet.FonePacketArray([pck3]))
        self.assertEqual(len(ppck.data()), 3)
        self.assertEqual(ppck.data()[0], ppck.data()[1])
        self.assertEqual(ppck.data()[0], ppck.data()[2])
        self.assertEqual(ppck.data()[0], 4.5)
