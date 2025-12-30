from PySide6 import QtWidgets


class OFnUIMain(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(OFnUIMain, self).__init__(parent=parent)
        central = QtWidgets.QWidget(self)
        central_layout = QtWidgets.QVBoxLayout(central)
        splitter = QtWidgets.QSplitter()
