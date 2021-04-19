    def openStudy(self):
        # TODO : create and show DialogOpenStudy, then intialiaze a new study
        dlg = DialogOpenStudy() # Could be renamed DialogCreateStudy
        res = dlg.exec()
        if (res == QtWidgets.QDialog.Accepted) :
            self.currentStudy = dlg.getStudy()
            self.currentStudy.loadSensors(self.sensorModel)
            self.currentStudy.loadPoints(self.pointModel)
            

    def importPoint(self):
        dlg = ImportPointDialog(self.currentStudy,self.sensorModel) 
        #for i in range(self.sensorModel.rowCount()) :
            #sensor_name = self.sensorModel.item(i).text() 
            #dlg.comboBox_Sensor.addItem(sensor_name)
        #for i in range(self.sensorModel.rowCount()) :
            #shaft_name = self.sensorModel.item(i).tcdext() 
            #dlg.comboBox_Shaft.addItem(shaft_name)
        res = dlg.exec()