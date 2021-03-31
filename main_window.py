# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(379, 294)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 379, 21))
        self.menubar.setObjectName("menubar")
        self.menuStudy = QtWidgets.QMenu(self.menubar)
        self.menuStudy.setObjectName("menuStudy")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockSensors = QtWidgets.QDockWidget(MainWindow)
        self.dockSensors.setObjectName("dockSensors")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.dockSensors.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockSensors)
        self.actionCreate_Study = QtWidgets.QAction(MainWindow)
        self.actionCreate_Study.setObjectName("actionCreate_Study")
        self.actionOpen_Study = QtWidgets.QAction(MainWindow)
        self.actionOpen_Study.setObjectName("actionOpen_Study")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuStudy.addAction(self.actionCreate_Study)
        self.menuStudy.addAction(self.actionOpen_Study)
        self.menuStudy.addSeparator()
        self.menuStudy.addAction(self.actionExit)
        self.menubar.addAction(self.menuStudy.menuAction())

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MOLONAVIZ"))
        self.menuStudy.setTitle(_translate("MainWindow", "Study"))
        self.actionCreate_Study.setText(_translate("MainWindow", "Create Study"))
        self.actionOpen_Study.setText(_translate("MainWindow", "Open Study"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
