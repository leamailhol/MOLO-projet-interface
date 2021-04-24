
import sys
import os
from PyQt5 import QtWidgets, uic
from study import Study

From_DialogOpenStudy,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogopenstudy.ui"))

class DialogOpenStudy(QtWidgets.QDialog,From_DialogOpenStudy):
    def __init__(self):
        # Call constructor of parent classes
        super(DialogOpenStudy, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)
        
        self.pushButtonBrowseStudy.clicked.connect(self.browseStudy)
        
        
    def browseStudy(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Study")
        if dirPath:
            self.lineEditStudy.setText(dirPath) 

    def getStudy(self):
        try : 
            path = self.lineEditStudy.text()
            dirs = os.listdir(path)
            for mydir in dirs:
                _, ext = os.path.splitext(mydir)
                if ext == '.txt':
                    f = open(path + f'/{mydir}',"r")
                    lines = f.readlines()
                    name = lines[0].rstrip('\n')
                    rootDir = lines[1].rstrip('\n')
                    sensorDir = lines[2].rstrip('\n')
                    return Study(name, rootDir, sensorDir)
        except TypeError as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Error detected : {e}")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec()
        except AttributeError as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Error detected : {e}, path invalid")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec()
        except PermissionError as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Error detected : {e}, path invalid on your computer")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec()
        except FileNotFoundError as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Error detected : {e}, folder invalid")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = DialogOpenStudy()
    mainWin.show()
    sys.exit(app.exec_())