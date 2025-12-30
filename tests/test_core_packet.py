import unittest
import numpy as np


class CorePacket(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from ofne.core import packet
        except:
            import sys
            import os
            sys.path.append((os.path.abspath(os.path.join(__file__, "../../python"))))
        finally:
            from ofne.core import packet
            from ofne import exceptions
            cls.packet = packet
            cls.exceptions = exceptions

    def testPacket(self):
        p = self.packet.OFnPacket()
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

        p2 = self.packet.OFnPacket(metadata={"a": 1}, data=np.array([1, 2, 3]))
        mt = p2.metadata()
        dt = p2.data()
        self.assertEqual(mt, {"a": 1})
        self.assertTrue(np.all(dt == np.array([1, 2, 3])))
        mt["a"] = 2
        dt[1] = 3
        self.assertEqual(mt, {"a": 2})
        self.assertTrue(np.all(dt == np.array([1, 3, 3])))
        self.assertEqual(p2.metadata(), {"a": 1})
        self.assertTrue(np.all(p2.data() == np.array([1, 2, 3])))
        self.assertFalse(np.all(p2.data() == dt))
        p3 = p2.copy()
        self.assertEqual(p3.metadata(), {"a": 1})
        self.assertTrue(np.all(p3.data() == np.array([1, 2, 3])))
        mt = p2.metadata()
        mt2 = p3.metadata()
        self.assertEqual(mt, mt2)
        mt2["a"] = 2
        self.assertNotEqual(mt, mt2)
        dt = p2.data()
        dt2 = p3.data()
        self.assertTrue(np.all(dt == dt2))
        dt[1] = 4
        self.assertFalse(np.all(dt == dt2))

        with self.assertRaises(self.exceptions.OFnInvalidArgumentError):
            self.packet.OFnPacket(metadata=["A", "b"])
        with self.assertRaises(self.exceptions.OFnInvalidArgumentError):
            self.packet.OFnPacket(data=[1, 2])

    def testPacketArray(self):
        p1 = self.packet.OFnPacket(metadata={"a": 1}, data=np.array([1, 2, 3]))
        pa1 = self.packet.OFnPacketArray([p1])
        self.assertIsNotNone(pa1)
        self.assertEqual(pa1.count(), 1)
        self.assertEqual(len(pa1.packet(0).data()), 3)
        self.assertEqual(len(pa1.packet(1).data()), 0)
        self.assertEqual(len(pa1.packet(1000).data()), 0)
        self.assertEqual(pa1.packet(0).data()[0], 1)
        self.assertEqual(pa1.packet(0).data()[1], 2)
        self.assertEqual(pa1.packet(0).data()[2], 3)
        self.assertEqual(pa1.packet(0).metadata().get("a", -1), 1)
        self.assertEqual(pa1.packet(1).metadata().get("a", -1), -1)
        self.assertEqual(pa1.packet(1000).metadata().get("a", -1), -1)

        p2 = self.packet.OFnPacket(metadata={"a": 2}, data=np.array([4, 5, 6]))
        pa2 = self.packet.OFnPacketArray([p1, p2])
        self.assertEqual(pa2.count(), 2)
        self.assertEqual(len(pa2.packet(0).data()), 3)
        self.assertEqual(len(pa2.packet(1).data()), 3)
        self.assertEqual(len(pa2.packet(2).data()), 0)
        self.assertEqual(len(pa2.packet(1000).data()), 0)
        self.assertEqual(pa2.packet(0).data()[0], 1)
        self.assertEqual(pa2.packet(0).data()[1], 2)
        self.assertEqual(pa2.packet(0).data()[2], 3)
        self.assertEqual(pa2.packet(1).data()[0], 4)
        self.assertEqual(pa2.packet(1).data()[1], 5)
        self.assertEqual(pa2.packet(1).data()[2], 6)
        self.assertEqual(pa2.packet(0).metadata().get("a", -1), 1)
        self.assertEqual(pa2.packet(1).metadata().get("a", -1), 2)
        self.assertEqual(pa2.packet(2).metadata().get("a", -1), -1)
        self.assertEqual(pa2.packet(1000).metadata().get("a", -1), -1)

        with self.assertRaises(self.exceptions.OFnInvalidArgumentError):
            self.packet.OFnPacketArray(p1)
        with self.assertRaises(self.exceptions.OFnInvalidArgumentError):
            self.packet.OFnPacketArray([p1, np.ndarray([7, 8, 9])])
