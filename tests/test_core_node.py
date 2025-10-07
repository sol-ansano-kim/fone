import unittest


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
            from fone import exceptions
            cls.node = node
            cls.exceptions = exceptions
            cls.param = param

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
                return 1

            def packetable(self):
                return True

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

        class EndOp(op.FoneOp):
            def __init__(self):
                super(End, self).__init__()

            def type(self):
                return self.__class__.__name__

            def params(self):
                return {}

            def needs(self):
                return 1

            def packetable(self):
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

            def needs(self):
                return 0

            def packetable(self):
                return True

        cls.OneInputs = OneInputs
        cls.ZeroInputs = ZeroInputs
        cls.TwoInputs = TwoInputs
        cls.ParamTester = ParamTester
        cls.EndOp = EndOp

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
