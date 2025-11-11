from . import abst


class FoneScene(abst._SceneBase):
    def __init__(self):
        super(FoneScene, self).__init__()
        self.__nodes = []

    def createNode(self, type, name=None):
        pass

    def deleteNode(self, node):
        pass

    def nodes(self):
        pass

    def getUniqueName(self, name):
        pass

    def read(self, filepath):
        pass

    def write(self, filepath):
        pass

    def clear(self):
        pass
