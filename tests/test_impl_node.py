import unittest
import numpy as np


class ImplNode(unittest.TestCase):
    @classmethod
    def setUp(cls):
        try:
            from fone.core import packet
        except:
            import sys
            import os
            sys.path.append((os.path.abspath(os.path.join(__file__, "../../python"))))
        finally:
            from fone.impl import _node
            from fone.core import op
            from fone.core import param
            from fone import exceptions
            cls._node = _node
            cls.exceptions = exceptions
            cls.param = param

        class OneInputs(op.FoneOp):
            def __init__(self):
                super(OneInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def params(self):
                return {}

            def requiredInputs(self):
                return 1

            def generateOutput(self):
                return True

        class ZeroInputs(op.FoneOp):
            def __init__(self):
                super(ZeroInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def params(self):
                return {}

            def requiredInputs(self):
                return 0

            def generateOutput(self):
                return True

        class TwoInputs(op.FoneOp):
            def __init__(self):
                super(TwoInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def params(self):
                return {}

            def requiredInputs(self):
                return 2

            def generateOutput(self):
                return False

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

            def requiredInputs(self):
                return 0

            def generateOutput(self):
                return True

        cls.OneInputs = OneInputs
        cls.ZeroInputs = ZeroInputs
        cls.TwoInputs = TwoInputs
        cls.ParamTester = ParamTester

    def test_op(self):
        i0 = self.ZeroInputs()
        i1 = self.OneInputs()
        i2 = self.TwoInputs()

        self.assertIsNotNone(i0)
        self.assertIsNotNone(i1)
        self.assertIsNotNone(i2)

        self.assertEqual(i0.type(), "ZeroInputs")
        self.assertEqual(i1.type(), "OneInputs")
        self.assertEqual(i2.type(), "TwoInputs")

        self.assertEqual(i0.requiredInputs(), 0)
        self.assertEqual(i1.requiredInputs(), 1)
        self.assertEqual(i2.requiredInputs(), 2)

        self.assertTrue(i0.generateOutput())
        self.assertTrue(i1.generateOutput())
        self.assertFalse(i2.generateOutput())

    def test_connect(self):
        i0 = self._node._FoneNodeImpl(self.ZeroInputs(), None)
        i1 = self._node._FoneNodeImpl(self.OneInputs(), None)

        self.assertTrue(i1.connectInput(0, i0))
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
        self.assertTrue(i1.connectInput(0, i0))
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(i1.inputs()[0], i0)
        self.assertEqual(len(i0.outputs()), 1)
        self.assertEqual(i0.outputs()[0], i1)

        self.assertTrue(i1.disconnectInput(0))
        self.assertEqual(len([x for x in i1.inputs() if x]), 0)
        self.assertEqual(len(i0.outputs()), 0)
        self.assertFalse(i1.disconnectInput(0))

        with self.assertRaises(self.exceptions.FoneIndexError):
            self.assertTrue(i1.connectInput(1, i0))
        with self.assertRaises(self.exceptions.FoneIndexError):
            self.assertTrue(i1.disconnectInput(1))

        i2 = self._node._FoneNodeImpl(self.TwoInputs(), None)
        self.assertTrue(i1.connectInput(0, i0))
        self.assertFalse(i1.connectInput(0, i2))
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(i1.inputs()[0], i0)

        i01 = self._node._FoneNodeImpl(self.ZeroInputs(), None)
        i02 = self._node._FoneNodeImpl(self.ZeroInputs(), None)
        i1 = self._node._FoneNodeImpl(self.OneInputs(), None)
        i2 = self._node._FoneNodeImpl(self.TwoInputs(), None)

        self.assertTrue(i1.connectInput(0, i01))
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(len(i01.outputs()), 1)
        self.assertEqual(len(i02.outputs()), 0)
        self.assertTrue(i1.connectInput(0, i02))
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(len(i01.outputs()), 0)
        self.assertEqual(len(i02.outputs()), 1)

        i2.connectInput(0, i02)
        i2.connectInput(1, i1)
        self.assertEqual(len([x for x in i1.inputs() if x]), 1)
        self.assertEqual(len(i02.outputs()), 2)
        self.assertEqual(len(i1.outputs()), 1)

        i2.disconnectAllInputs()
        self.assertEqual(len([x for x in i2.inputs() if x]), 0)
        self.assertEqual(len(i02.outputs()), 1)
        self.assertEqual(len(i1.outputs()), 0)
        i1.disconnectAllInputs()
        self.assertEqual(len(i02.outputs()), 0)
        self.assertEqual(len([x for x in i1.inputs() if x]), 0)

    def test_params(self):
        pt = self.ParamTester()
        pt1 = self._node._FoneNodeImpl(pt, None)
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
