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

        class ZeroInputs(op.FoneOp):
            def __init__(self):
                super(ZeroInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def requiredInputs(self):
                return 0

        class TwoInputs(op.FoneOp):
            def __init__(self):
                super(TwoInputs, self).__init__()

            def type(self):
                return self.__class__.__name__

            def requiredInputs(self):
                return 2

        cls.OneInputs = OneInputs
        cls.ZeroInputs = ZeroInputs
        cls.TwoInputs = TwoInputs

    def test_creating(self):
        oi = self.OneInputs()
        zi = self.ZeroInputs()
        tw = self.TwoInputs()

        self.assertIsNotNone(oi)
        self.assertIsNotNone(zi)
        self.assertIsNotNone(tw)
