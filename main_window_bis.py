import sys
import os
from PyQt5 import QtWidgets, uic

From_MainWindow,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"main_window.ui"))
class MainWindow(QtWidgets.QMainWindow,From_MainWindow):
    def __init__(self):
        # Call constructor of parent classes
        super(MainWindow, self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

