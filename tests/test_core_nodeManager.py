import unittest


class NodeManagerTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        try:
            from fone.core import nodeManager
        except:
            import sys
            sys.path.append((os.path.abspath(os.path.join(__file__, "../../python"))))
        finally:
            import os
            from fone.core import nodeManager
            cls.nodeManager = nodeManager
            cls.orgEnv = os.environ.get("FONE_PLUGIN_PATH")
            os.environ["FONE_PLUGIN_PATH"] = os.path.join(__file__, "../plugins")

    @classmethod
    def tearDown(cls):
        import os

        if not cls.orgEnv:
            os.environ.pop("FONE_PLUGIN_PATH", None)
        else:
            os.environ["FONE_PLUGIN_PATH"] = cls.orgEnv

    def test_singleton(self):
        a = self.nodeManager.FoneNodeManager()
        self.assertIsNotNone(a)
        b = self.nodeManager.FoneNodeManager()
        self.assertIsNotNone(a)
        self.assertEqual(a, b)
        self.assertEqual(id(a), id(b))
