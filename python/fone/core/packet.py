import copy
import numpy as np
from .. import exceptions


class FonePacket(object):
    def __init__(self, metadata=None, data=None):
        super(FonePacket, self).__init__()
        self.__metadata = {}
        self.__data = np.array([])

        if isinstance(metadata, dict):
            self.__metadata = metadata.copy()
        elif metadata is not None:
            raise exceptions.FoneInvalidArgumentError(dict, metadata)

        if isinstance(data, np.ndarray):
            self.__data = data.copy()
        elif data is not None:
            raise exceptions.FoneInvalidArgumentError(np.ndarray, data)

    def copy(self):
        return FonePacket(metadata=self.__metadata, data=self.__data)

    def metadata(self):
        return copy.deepcopy(self.__metadata)

    def data(self):
        return self.__data.copy()


class FonePacketArray(object):
    def __init__(self, packets):
        super(FonePacketArray, self).__init__()
        if not isinstance(packets, list):
            raise exceptions.FoneInvalidArgumentError(list, packets)
        for fp in packets:
            if not isinstance(fp, FonePacket):
                raise exceptions.FoneInvalidArgumentError(FonePacket, fp)

        self.__packets = packets[:]
        self.__count = len(packets)

    def count(self):
        return self.__count

    def packet(self, index):
        if index >= self.__count:
            return FonePacket()

        return self.__packets[index]
