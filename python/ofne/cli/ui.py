import os
import sys
from PySide6 import QtWidgets

try:
    import fone.ui
except:
    sys.path.append(os.path.abspath(os.path.join(__file__, "../../..")))
    import fone.ui


def main():
    app = QtWidgets.QApplication(sys.argv)

    win = fone.ui.MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
