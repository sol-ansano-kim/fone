from . import abst
class FoneScene(abst._SceneBase):
    __INSTANCE = None

    def __new__(self):
        if FoneScene.__INSTANCE is None:
            FoneScene.__INSTANCE = super(FoneScene, self).__new__(self)
            FoneScene.__INSTANCE.__initialize()

        return FoneScene.__INSTANCE

    def __init__(self):
        super(FoneScene, self).__init__()

    def __initialize(self):
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
