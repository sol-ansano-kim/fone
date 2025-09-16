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
            from fone import exceptions
            cls._node = _node
            cls.exceptions = exceptions

        class OneInputs(op.FoneOp):
            def __init__(self):
                super(OneInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def requiredInputs(self):
                return 1

            def generateOutput(self):
                return True

        class ZeroInputs(op.FoneOp):
            def __init__(self):
                super(ZeroInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def requiredInputs(self):
                return 0

            def generateOutput(self):
                return True

        class TwoInputs(op.FoneOp):
            def __init__(self):
                super(TwoInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def requiredInputs(self):
                return 2

            def generateOutput(self):
                return False

        cls.OneInputs = OneInputs
        cls.ZeroInputs = ZeroInputs
        cls.TwoInputs = TwoInputs

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

    def test_connect1(self):
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
