import unittest


class SceneTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        try:
            from fone.core import scene
        except:
            import sys
            sys.path.append((os.path.abspath(os.path.join(__file__, "../../python"))))
        finally:
            import os
            from fone.core import scene
            cls.scene = scene
            cls.orgEnv = os.environ.get("FONE_PLUGIN_PATH")
            os.environ["FONE_PLUGIN_PATH"] = os.path.join(__file__, "../plugins")

    @classmethod
    def tearDown(cls):
        import os

        if not cls.orgEnv:
            os.environ.pop("FONE_PLUGIN_PATH", None)
        else:
            os.environ["FONE_PLUGIN_PATH"] = cls.orgEnv

    def test_create(self):
        scn = self.scene.FoneScene()
        self.assertIsNotNone(scn)
        self.assertEqual(scn.nodes(), [])
        nodea = scn.createNode("MyOpA")
        self.assertIsNotNone(nodea)
        self.assertEqual(len(scn.nodes()), 1)
        self.assertEqual(nodea.name(), "MyOpA")
        nodeb = scn.createNode("MyOpB")
        self.assertIsNotNone(nodeb)
        self.assertEqual(len(scn.nodes()), 2)
        self.assertEqual(nodeb.name(), "MyOpB")
        nodec = scn.createNode("MyOpC")
        self.assertIsNone(nodec)
        self.assertEqual(len(scn.nodes()), 2)
        nodea2 = scn.createNode("MyOpA")
        self.assertIsNotNone(nodea2)
        self.assertEqual(len(scn.nodes()), 3)
        self.assertEqual(nodea2.name(), "MyOpA1")
        nodea3 = scn.createNode("MyOpA")
        self.assertIsNotNone(nodea3)
        self.assertEqual(len(scn.nodes()), 4)
        self.assertEqual(nodea3.name(), "MyOpA2")

        scn = self.scene.FoneScene()
        n = scn.createNode("MyOpB", name="aaa")
        self.assertEqual(len(scn.nodes()), 1)
        self.assertEqual(n.name(), "aaa")
        n = scn.createNode("MyOpB", name="aaa")
        self.assertEqual(len(scn.nodes()), 2)
        self.assertEqual(n.name(), "aaa1")

    def test_delete(self):
        scn = self.scene.FoneScene()
        a = scn.createNode("MyOpB", name="a")
        b = scn.createNode("MyOpB", name="b")
        c = scn.createNode("MyOpB", name="c")
        self.assertEqual(len(scn.nodes()), 3)
        self.assertTrue(scn.deleteNode(b))
        self.assertEqual(len(scn.nodes()), 2)

        scn2 = self.scene.FoneScene()
        a = scn2.createNode("MyOpB", name="a")
        self.assertEqual(len(scn.nodes()), 2)
        self.assertEqual(len(scn2.nodes()), 1)

        self.assertFalse(scn.deleteNode(a))
        self.assertFalse(scn2.deleteNode(c))
        self.assertEqual(len(scn.nodes()), 2)
        self.assertEqual(len(scn2.nodes()), 1)

        self.assertTrue(scn.deleteNode(c))
        self.assertTrue(scn2.deleteNode(a))
        self.assertEqual(len(scn.nodes()), 1)
        self.assertEqual(len(scn2.nodes()), 0)

    def test_node(self):
        scn = self.scene.FoneScene()
        scn.createNode("MyOpA", name="a")
        scn.createNode("MyOpA", name="a")
        scn.createNode("MyOpB", name="a")
        self.assertEqual([x.name() for x in scn.nodes()], ["a", "a1", "a2"])
        nodes = scn.nodes()
        nodes.pop(1)
        self.assertEqual([x.name() for x in nodes], ["a", "a2"])
        self.assertEqual([x.name() for x in scn.nodes()], ["a", "a1", "a2"])

    def test_clear(self):
        scn = self.scene.FoneScene()
        scn.createNode("MyOpA", name="a")
        scn.createNode("MyOpA", name="a")
        scn.createNode("MyOpB", name="a")
        self.assertEqual([x.name() for x in scn.nodes()], ["a", "a1", "a2"])
        self.assertTrue(scn.clear())
        self.assertEqual([x.name() for x in scn.nodes()], [])
