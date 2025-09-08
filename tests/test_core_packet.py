import unittest
import numpy as np


class CorePacket(unittest.TestCase):
    @classmethod
    def setUp(cls):
        try:
            from fone.core import packet
        except:
            import sys
            import os
            sys.path.append((os.path.abspath(os.path.join(__file__, "../../python"))))
        finally:
            from fone.core import packet
            from fone import exceptions
            cls.packet = packet
            cls.exceptions = exceptions

    def test_packet_1(self):
        p = self.packet.FonePacket()
        self.assertIsNotNone(p)
        self.assertTrue(isinstance(p.metadata(), dict))
        self.assertTrue(isinstance(p.data(), np.ndarray))
        mt = p.metadata()
        dt = p.data()
        self.assertEqual(len(mt), 0)
        self.assertEqual(len(dt), 0)
        mt[1] = 2
        dt = np.append(dt, 1)
        self.assertEqual(len(mt), 1)
        self.assertEqual(len(dt), 1)
        self.assertEqual(len(p.metadata()), 0)
        self.assertEqual(len(p.data()), 0)

        p2 = self.packet.FonePacket(metadata={"a": 1}, data=np.array([1, 2, 3]))
        mt = p2.metadata()
        dt = p2.data()
        self.assertEqual(mt, {"a": 1})
        self.assertTrue(np.all(dt == np.array([1, 2, 3])))
        mt["a"] = 2
        dt *= np.array([1, 2, 3])
        self.assertEqual(mt, {"a": 2})
        self.assertTrue(np.all(dt == np.array([1, 4, 9])))
        self.assertEqual(p2.metadata(), {"a": 1})
        self.assertTrue(np.all(p2.data() == np.array([1, 2, 3])))
        p3 = p2.copy()
        self.assertEqual(p3.metadata(), {"a": 1})
        self.assertTrue(np.all(p3.data() == np.array([1, 2, 3])))
        mt = p2.metadata()
        mt2 = p3.metadata()
        self.assertEqual(mt, mt2)
        mt2["a"] = 2
        self.assertNotEqual(mt, mt2)

        with self.assertRaises(self.exceptions.FoneInvalidArgument):
            self.packet.FonePacket(metadata=["A", "b"])
        with self.assertRaises(self.exceptions.FoneInvalidArgument):
            self.packet.FonePacket(data=[1, 2])
