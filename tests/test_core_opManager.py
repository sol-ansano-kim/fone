import unittest


class NodeManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from fone.core import opManager
        except:
            import sys
            sys.path.append((os.path.abspath(os.path.join(__file__, "../../python"))))
        finally:
            import os
            from fone.core import opManager
            from fone.core import op
            cls.op = op
            cls.opManager = opManager
            cls.orgEnv = os.environ.get("FONE_PLUGIN_PATH")
            os.environ["FONE_PLUGIN_PATH"] = os.path.join(__file__, "../plugins")

            class TestOpA(op.FoneOp):
                pass

            class TestOpB(op.FoneOp):
                pass

            cls.TestOpA = TestOpA
            cls.TestOpB = TestOpB

            cls.opManager.FoneOpManager().reloadPlugins()

    @classmethod
    def tearDownClass(cls):
        import os

        if not cls.orgEnv:
            os.environ.pop("FONE_PLUGIN_PATH", None)
        else:
            os.environ["FONE_PLUGIN_PATH"] = cls.orgEnv

        cls.opManager.FoneOpManager().reloadPlugins()

    def test_singleton(self):
        a = self.opManager.FoneOpManager()
        self.assertIsNotNone(a)
        b = self.opManager.FoneOpManager()
        self.assertIsNotNone(a)
        self.assertEqual(a, b)
        self.assertEqual(id(a), id(b))

    def test_load(self):
        man = self.opManager.FoneOpManager()
        man.reloadPlugins()
        self.assertEqual(man.listOps(), ["MyOpA", "MyOpB"])
        op = man.getOp("MyOpA")
        self.assertIsNotNone(op)
        op = man.getOp("MyOpB")
        self.assertIsNotNone(op)
        op = man.getOp("MyOpC")
        self.assertIsNone(op)

    def test_reg_dereg(self):
        man = self.opManager.FoneOpManager()
        self.assertEqual(len(man.listOps()), 2)
        opa = self.TestOpA()
        opa1 = self.TestOpA()
        opb = self.TestOpB()

        self.assertTrue(man.registerOp(opa))
        self.assertEqual(len(man.listOps()), 3)
        self.assertEqual(man.getOp("TestOpA"), opa)
        self.assertFalse(man.registerOp(opa))
        self.assertEqual(len(man.listOps()), 3)
        self.assertFalse(man.registerOp(opa1))
        self.assertNotEqual(man.getOp("TestOpA"), opa1)
        self.assertEqual(len(man.listOps()), 3)
        self.assertTrue(man.registerOp(opb))
        self.assertEqual(len(man.listOps()), 4)
        self.assertEqual(man.getOp("TestOpB"), opb)
        self.assertTrue(man.deregisterOp(opb))
        self.assertEqual(len(man.listOps()), 3)
        self.assertFalse(man.deregisterOp(opb))
        self.assertEqual(len(man.listOps()), 3)
        self.assertFalse(man.deregisterOp(opa1))
        self.assertEqual(len(man.listOps()), 3)
        self.assertTrue(man.deregisterOp(opa))
        self.assertEqual(len(man.listOps()), 2)
