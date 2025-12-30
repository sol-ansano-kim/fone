import copy
import numpy as np
from . import abst
from .. import exceptions


class OFnPacket(abst._PacketBase):
    def __init__(self, metadata=None, data=None):
        super(OFnPacket, self).__init__()
        self.__metadata = {}
        self.__data = np.array([])

        if isinstance(metadata, dict):
            self.__metadata = metadata.copy()
        elif metadata is not None:
            raise exceptions.OFnInvalidArgumentError(dict, metadata)

        if isinstance(data, np.ndarray):
            self.__data = data.copy()
        elif data is not None:
            raise exceptions.OFnInvalidArgumentError(np.ndarray, data)

    def copy(self):
        return OFnPacket(metadata=self.__metadata, data=self.__data)

    def metadata(self):
        return copy.deepcopy(self.__metadata)

    def data(self):
        return self.__data.copy()


class OFnPacketArray(abst._PacketArrayBase):
    def __init__(self, packets):
        super(OFnPacketArray, self).__init__()
        if not isinstance(packets, list):
            raise exceptions.OFnInvalidArgumentError(list, packets)
        for fp in packets:
            if not isinstance(fp, OFnPacket):
                raise exceptions.OFnInvalidArgumentError(OFnPacket, fp)

        self.__packets = packets[:]
        self.__count = len(packets)

    def count(self):
        return self.__count

    def packet(self, index):
        if index >= self.__count:
            return OFnPacket()

        return self.__packets[index]
