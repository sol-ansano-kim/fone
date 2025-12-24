import copy
import numpy as np
from . import abst
from .. import exceptions


class FnCorePacket(abst._PacketBase):
    def __init__(self, metadata=None, data=None):
        super(FnCorePacket, self).__init__()
        self.__metadata = {}
        self.__data = np.array([])

        if isinstance(metadata, dict):
            self.__metadata = metadata.copy()
        elif metadata is not None:
            raise exceptions.FnErrInvalidArgumentError(dict, metadata)

        if isinstance(data, np.ndarray):
            self.__data = data.copy()
        elif data is not None:
            raise exceptions.FnErrInvalidArgumentError(np.ndarray, data)

    def copy(self):
        return FnCorePacket(metadata=self.__metadata, data=self.__data)

    def metadata(self):
        return copy.deepcopy(self.__metadata)

    def data(self):
        return self.__data.copy()


class FnCorePacketArray(abst._PacketArrayBase):
    def __init__(self, packets):
        super(FnCorePacketArray, self).__init__()
        if not isinstance(packets, list):
            raise exceptions.FnErrInvalidArgumentError(list, packets)
        for fp in packets:
            if not isinstance(fp, FnCorePacket):
                raise exceptions.FnErrInvalidArgumentError(FnCorePacket, fp)

        self.__packets = packets[:]
        self.__count = len(packets)

    def count(self):
        return self.__count

    def packet(self, index):
        if index >= self.__count:
            return FnCorePacket()

        return self.__packets[index]
