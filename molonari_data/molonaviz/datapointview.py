import os
from point import Point
import pandas as pd 
from study import Study
from csv import reader
from sensor import pressureSensor
import numpy as np
from pyheatmy import *
from datetime import datetime


import sys
import matplotlib.pyplot as plt
import matplotlib.backends
from matplotlib.backends import backend_qt5agg
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtWidgets

From_DataPointView,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"datapointview.ui"))


from dialogcleanup import DialogCleanUp
from numpy import NaN
from computedialog import ComputeDialog
from pyheatmy import *


#path_point = 'C:/Users/Léa/Documents/MINES 2A/MOLONARI/INTERFACE/MOLO-projet-interface/molonari_data/study_ordiLea/Point001'
#os.chdir(path_point)
# Create processed temperatures plot

class TimeSeriesPlotCanvas(matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg):

    def __init__(self, title, y_name, variable):
        
        self.variable = variable
        self.fig = matplotlib.figure.Figure()
        self.title = title
        self.axes = self.fig.add_subplot(111)
        self.ylab = y_name
        
        

        matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg.__init__(self,self.fig)


    def setModel(self, model):

        self.model = model
    
    def plot(self):

        
        self.axes.cla()

        if self.variable == 'Temperature': 
            self.axes.title.set_text(self.title)
            self.axes.set_xlabel('Time')
            self.axes.set_ylabel(self.ylab)
            data = self.model.getData()
            self.axes.plot(data['Date'], data['T sensor 1'], label = '10cm')
            self.axes.plot(data['Date'], data['T sensor 2'], label = '20cm')
            self.axes.plot(data['Date'], data['T sensor 3'], label = '30cm')
            self.axes.plot(data['Date'], data['T sensor 4'], label = '40cm')
            self.axes.set_xticklabels(data['Date'], rotation=45)
            self.axes.legend()
            self.draw()
        
        if self.variable == 'Pressure':
            self.axes.title.set_text(self.title)
            self.axes.set_xlabel('Time')
            self.axes.set_ylabel(self.ylab)
            data = self.model.getData()
            self.axes.plot(data['Date'], data['Pressure'])
            self.axes.set_xticklabels(data['Date'], rotation=45)
            self.draw()

        if self.variable =='MatrixTemp':

            self.axes.title.set_text(self.title)
            self.axes.set_xlabel('Depth')
            self.axes.set_ylabel(self.ylab)
            data = np.array(self.model.getData())
            matrix = np.delete(data,0,1)
            im = self.axes.imshow(matrix, aspect='auto')
            self.fig.colorbar(im)
            self.draw()

        if self.variable == 'DepthDirectTemp':

            self.axes.title.set_text(self.title)
            self.axes.set_xlabel('Temperature')
            self.axes.set_ylabel(self.ylab)
            data = self.model.getData()
            row1 = np.array(data.columns )
            data = np.vstack((row1,np.array(data)))
            data = np.delete(data,0,1)
            self.axes.plot(data[1,:], data[0,:], label = 'Time 1')
            self.axes.plot(data[2,:], data[0,:], label = 'Time 2')
            self.axes.plot(data[3,:], data[0,:], label = 'Time 3')
            self.axes.plot(data[4,:], data[0,:], label = 'Time 4')
            self.axes.legend()
            self.axes.set_yticks(np.arange(0,99, 10))
            self.axes.invert_yaxis()
            self.draw()
        
        
        if self.variable == 'DirectFlow':
            
            
            self.axes.title.set_text(self.title)
            self.axes.set_xlabel('Time')
            self.axes.set_ylabel(self.ylab)
            data = self.model.getData()
            data_tab = np.array(data)
            print(data_tab)
            print(data_tab[:][1])
            print()
            self.axes.plot(data['0'] ,data['1'])
            self.draw()

        if self.variable =='MatrixTempInv':

            self.axes.title.set_text(self.title)
            self.axes.set_xlabel('Depth')
            self.axes.set_ylabel(self.ylab)
            data = np.array(self.model.getData())
            matrix = np.delete(data,0,1)
            im = self.axes.imshow(matrix, aspect='auto')
            self.fig.colorbar(im)
            self.draw()
        
        if self.variable == 'DepthDirectTempInv':

            self.axes.title.set_text(self.title)
            self.axes.set_xlabel('Temperature')
            self.axes.set_ylabel(self.ylab)
            data = self.model.getData()
            row1 = np.array(data.columns )
            data = np.vstack((row1,np.array(data)))
            data = np.delete(data,0,1)
            self.axes.plot(data[1,:], data[0,:], label = 'Time 1')
            self.axes.plot(data[2,:], data[0,:], label = 'Time 2')
            self.axes.plot(data[3,:], data[0,:], label = 'Time 3')
            self.axes.plot(data[4,:], data[0,:], label = 'Time 4')
            self.axes.legend()
            self.axes.set_yticks(np.arange(0, 40, 10))
            self.axes.invert_yaxis()
            self.draw()

        
           







class pandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None
    
    def getData(self):
        return self._data


class DataPointView(QtWidgets.QDialog,From_DataPointView):
    def __init__(self,point,currentStudy,sensorModel):
        # Call constructor of parent classes
        super(DataPointView, self).__init__()
        QtWidgets.QDialog.__init__(self)
        self.path_point = point.path
        self.point = point
        os.chdir(self.path_point)
        self.setupUi(self)
        self.currentStudy = currentStudy
        self.sensorModel = sensorModel
        self.compdlg = None
        self.col = None
        self.dataPressure = None
        self.dataTemperature = None 

        # On paramètre le premier onglet
        self.unit = self.comboBox_TempUnit.currentText()
        self.lineEdit_Pressure.setText(self.point.pressure_sensor)
        self.lineEdit_Shaft.setText(self.point.shaft)
        file = open(self.point.info,"r")
        lines = file.readlines()
        for line in lines:
            if line.split(';')[0].strip() == "Meas_Date":
                meas_date = line.split(';')[1].strip()
        self.lineEdit_Date.setText(meas_date)

        ## Notice

        text_notice = ''

        with open('imp_notice.csv', 'r', encoding='utf8') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                if len(row) > 0 and text_notice!='': 
                    # row variable is a list that represents a row in csv
                    text_notice = text_notice + '\n' + row[0]
                if len(row) > 0 and text_notice == '':
                    text_notice = row[0]


        self.plainTextEditNotice.appendPlainText(text_notice)
        self.plainTextEditNotice.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)


        ## Geometrie 

        print('')

        text_geometry = ''

        with open('imp_info.csv', 'r', encoding='utf8') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                if len(row) > 0 and text_geometry!='': 
                    # row variable is a list that represents a row in csv
                    word1, word2 = row[0].split(';') 
                    text_geometry = text_geometry + '\n' + word1 + ' : ' + word2
                if len(row) > 0 and text_geometry == '':
                    word1, word2 = row[0].split(';') 
                    text_geometry= 'Point_Name : ' + word2
        
        self.plainTextEditGeometry.appendPlainText(text_geometry)
        self.plainTextEditGeometry.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        ## Info

        self.InstallationImage.setPixmap(QtGui.QPixmap('imp_config.png'))
        self.pushButtonReset.clicked.connect(self.reset)
        self.pushButtonCleanup.clicked.connect(self.cleanup)
        self.pushButtonCompute.clicked.connect(self.compute)

        self.comboBox_TempUnit.currentTextChanged.connect(self.changeunit)
        self.checkBox_Raw.stateChanged.connect(self.showrawdata)

        #Temperature
        if self.checkBox_Raw.isChecked() :
            col_temp = ['Index','Date','T sensor 1','T sensor 2', 'T sensor 3', 'T sensor 4']
            self.dataTemperature = pd.read_csv('imp_raw_temperature.csv', encoding='utf-8', sep=';', low_memory=False, skiprows=1)
            self.dataTemperature.columns = col_temp
            self.dataTemperature.index.name='Index'
            if self.unit == '°C' :
                for i in range(1,5) :
                    self.dataTemperature[f'T sensor {i}'] = self.dataTemperature[f'T sensor {i}'] - float(273.5)
        else : 
            self.dataTemperature = pd.read_csv('processed_temperature.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
            if self.unit == '°C' :
                for i in range(1,5) :
                    self.dataTemperature[f'T sensor {i}'] = self.dataTemperature[f'T sensor {i}'] - float(273.5)
        data_to_display_temp = pandasModel(self.dataTemperature)
        self.tableViewTemperature.setModel(data_to_display_temp)

        # Récupération des datas 
        self.dataTemperature = pd.read_csv('processed_temperature.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
        
        #Pressure
        if self.checkBox_Raw.isChecked() :
            self.dataPressure = pd.read_csv('imp_raw_pressure.csv', encoding='utf-8', sep=';', low_memory=False, skiprows=0)
            if self.unit == '°C' :
                self.dataPressure['Temperature'] = self.dataPressure['Temperature']- float(273.5)
        else :
            self.dataPressure = pd.read_csv('processed_pressure.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
            if self.unit == '°C' :
                self.dataPressure['Temperature'] = self.dataPressure['Temperature']- float(273.5)
        data_to_display_press = pandasModel(self.dataPressure)
        self.tableViewPressure.setModel(data_to_display_press)

        #Plot 
        self.plotViewTemp = TimeSeriesPlotCanvas("Temperature evolution", "Temperature", 'Temperature') # Titre du grahique + indice des séries à afficher (=  colonnes dans le data frame)
        self.layoutMeasuresTemp.addWidget(self.plotViewTemp)
        self.plotViewTemp.setModel(data_to_display_temp)
        self.plotViewTemp.plot()


        self.plotViewPress = TimeSeriesPlotCanvas("Pressure evolution", "Pressure (Bar)", 'Pressure') # Titre du grahique + indice des séries à afficher (=  colonnes dans le data frame)
        self.layoutMeasuresTemp.addWidget(self.plotViewPress)
        self.plotViewPress.setModel(data_to_display_press)
        self.plotViewPress.plot()

        self.dataDirectTemp = pd.read_csv('res_temps.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
        data_to_display_directTemp = pandasModel(self.dataDirectTemp)

        self.DirectViewMat = TimeSeriesPlotCanvas("Temperature's Matrix", "Time", 'MatrixTemp')
        self.layoutDirect.addWidget(self.DirectViewMat)
        self.DirectViewMat.setModel(data_to_display_directTemp)
        self.DirectViewMat.plot()

        self.DirectViewDep = TimeSeriesPlotCanvas("Temperature profile", "Depth", 'DepthDirectTemp')
        self.layoutDirect.addWidget(self.DirectViewDep)
        self.DirectViewDep.setModel(data_to_display_directTemp)
        self.DirectViewDep.plot()

        self.dataDirectFlow = pd.read_csv('res_flows.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
        data_to_display_directFlow = pandasModel(self.dataDirectFlow)
        self.tableViewPressure.setModel(data_to_display_directFlow)


        self.DirectViewDepFlow = TimeSeriesPlotCanvas("Flow evolution", "Flow", 'DirectFlow')
        self.layoutDirect.addWidget(self.DirectViewDepFlow)
        self.DirectViewDepFlow.setModel(data_to_display_directFlow)
        self.DirectViewDepFlow.plot()

        self.dataInvTemp = pd.read_csv('res_temps_50.0.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
        data_to_display_invTemp = pandasModel(self.dataInvTemp)

        self.InvViewMat = TimeSeriesPlotCanvas("Temperature's Matrix", "Time", 'MatrixTempInv')
        self.layoutInv.addWidget(self.InvViewMat)
        self.InvViewMat.setModel(data_to_display_invTemp)
        self.InvViewMat.plot()

        self.InvViewDep = TimeSeriesPlotCanvas("Temperature profile", "Depth", 'DepthDirectTempInv')
        self.layoutInv.addWidget(self.InvViewDep)
        self.InvViewDep.setModel(data_to_display_invTemp)
        self.InvViewDep.plot()


    def changeunit(self) :
        self.unit = self.comboBox_TempUnit.currentText()
        if self.unit == '°C' :
            for i in range(1,5) :
                self.dataTemperature[f'T sensor {i}'] = self.dataTemperature[f'T sensor {i}'] - float(273.5)
            self.dataPressure['Temperature'] = self.dataPressure['Temperature']- float(273.5)
        else :
            for i in range(1,5) :
                self.dataTemperature[f'T sensor {i}'] = self.dataTemperature[f'T sensor {i}'] + float(273.5)
            self.dataPressure['Temperature'] = self.dataPressure['Temperature'] + float(273.5)
        data_to_display_temp = pandasModel(self.dataTemperature)
        self.tableViewTemperature.setModel(data_to_display_temp)
        data_to_display_press = pandasModel(self.dataPressure)
        self.tableViewPressure.setModel(data_to_display_press)

        self.layoutMeasuresTemp.addWidget(self.plotViewTemp)
        self.plotViewTemp.setModel(data_to_display_temp)
        self.plotViewTemp.plot()
    
    def showrawdata(self) :
        #Pres
        if self.checkBox_Raw.isChecked() :
            col_press = ['Date','Tension','Temperature']
            self.dataPressure = pd.read_csv('imp_raw_pressure.csv', encoding='utf-8', sep=';', low_memory=False, skiprows=0)
            self.dataPressure.columns = col_press
            self.dataPressure.index.name='Index'
            self.dataPressure = self.dataPressure.dropna()
            self.dataPressure = self.dataPressure.astype({'Temperature': np.float})
            if self.unit == '°C' :
                self.dataPressure['Temperature'] = self.dataPressure['Temperature']- float(273.5)
        else :
            self.dataPressure = pd.read_csv('processed_pressure.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
            if self.unit == '°C' :
                self.dataPressure['Temperature'] = self.dataPressure['Temperature'] - float(273.5)
        data_to_display_press = pandasModel(self.dataPressure)
        self.tableViewPressure.setModel(data_to_display_press)
        #Temp
        if self.checkBox_Raw.isChecked() :
            col_temp = ['Index','Date','T sensor 1','T sensor 2', 'T sensor 3', 'T sensor 4']
            self.dataTemperature = pd.read_csv('imp_raw_temperature.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=1)
            self.dataTemperature.columns = col_temp
            self.dataTemperature.index.name='Index'
            self.dataTemperature = self.dataTemperature.dropna()
            self.dataTemperature = self.dataTemperature.astype({'T sensor 1': np.float,'T sensor 2': np.float,'T sensor 3': np.float,'T sensor 4': np.float})
            if self.unit == 'K' :
                for i in range(1,5) :
                    self.dataTemperature[f'T sensor {i}'] = self.dataTemperature[f'T sensor {i}'] + float(273.5)
        else : 
            self.dataTemperature = pd.read_csv('processed_temperature.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
            if self.unit == '°C' :
                for i in range(1,5) :
                    self.dataTemperature[f'T sensor {i}'] = self.dataTemperature[f'T sensor {i}'] - float(273.5)
        data_to_display_temp = pandasModel(self.dataTemperature)
        self.tableViewTemperature.setModel(data_to_display_temp)
        


    def reset(self):
        print('reset')
    
    def cleanup(self):
        clnp = DialogCleanUp() 
        res = clnp.exec()
        if (res == QtWidgets.QDialog.Accepted) :
            mycleanupcode = clnp.getCode()
            print(mycleanupcode)
            clnp.saveCleanedUpData(mycleanupcode)
            
            self.dataTemperature = pd.read_csv('processed_temperature.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
            data_to_display_temp = pandasModel(self.dataTemperature)
            self.tableViewTemperature.setModel(data_to_display_temp)
            
            
            self.dataPressure = pd.read_csv('processed_pressure.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
            data_to_display_press = pandasModel(self.dataPressure)
            self.tableViewPressure.setModel(data_to_display_press)


            self.layoutMeasuresTemp.addWidget(self.plotViewTemp)
            self.plotViewTemp.setModel(data_to_display_temp)
            self.plotViewTemp.plot()

            self.layoutMeasuresTemp.addWidget(self.plotViewPress)
            self.plotViewPress.setModel(data_to_display_press)
            self.plotViewPress.plot()

            

    def compute(self):
        self.compdlg = ComputeDialog()
        self.compdlg.pushButton_RunModel.clicked.connect(self.runmodel)
        self.compdlg.pushButton_Inversion.clicked.connect(self.runinversion)
        self.compdlg.exec()
            

    def runmodel(self) :
        dicParam = self.create_dicParam()
        print(dicParam)
        computeSolveTransi = self.create_computeSolveTransi()
        print(computeSolveTransi)
        self.col = Column.from_dict(dicParam)
        params_tuple = computeSolveTransi[0]
        self.col.compute_solve_transi(params_tuple, computeSolveTransi[1])
        time = self.col.get_times_solve()
        dftime = pd.DataFrame(time)
        dftime.to_csv(f'{self.path_point}/res_time.csv')
        depths = self.col.get_depths_solve()
        dfdepths = pd.DataFrame(depths)
        dfdepths.to_csv(f'{self.path_point}/res_depths.csv')
        temps = self.col.get_temps_solve()
        dftemps = pd.DataFrame(temps)
        dftemps.to_csv(f'{self.path_point}/res_temps.csv')
        flows = self.col.get_flows_solve()
        dfflows = pd.DataFrame(flows)
        dfflows.to_csv(f'{self.path_point}/res_flows.csv')
        #advec = self.col.get_advec_flows_solve()
        #dfadvec = pd.DataFrame(advec)
        #dfadvec.to_csv(f'{self.path_point}/res_advec.csv')
        #conduc = self.col.get_conduc_flows_solve() 
        #dfconduc = pd.DataFrame(conduc)
        #dfconduc.to_csv(f'{self.path_point}/res_conduc.csv')
        

    def runinversion(self) :
        paramMCMC = self.create_paramMCMC()
        print(paramMCMC)
        self.col.compute_mcmc(nb_iter = paramMCMC[1], priors = paramMCMC[0], nb_cells = paramMCMC[2])
        all_params = self.col.get_all_params()
        dfparams = pd.DataFrame(all_params)
        dfparams.to_csv(f'{self.path_point}/res_all_params.csv')
        #best_params = self.col.get_best_param()
        #dfbest = pd.DataFrame(best_params)
        #dfbest.to_csv(f'{self.path_point}/res_best_params.csv')
        moinslog10K = self.col.get_all_moinslog10K()
        dfK = pd.DataFrame(moinslog10K)
        dfK.to_csv(f'{self.path_point}/res_all_moinslog10K.csv')
        lambda_s = self.col.get_all_lambda_s()
        dflambda = pd.DataFrame(lambda_s)
        dflambda.to_csv(f'{self.path_point}/res_all_lambda_s.csv')
        n = self.col.get_all_n()
        dfn = pd.DataFrame(n)
        dfn.to_csv(f'{self.path_point}/res_all_n.csv')
        rho = self.col.get_all_rhos_cs()
        dfrho = pd.DataFrame(rho)
        dfrho.to_csv(f'{self.path_point}/res_all_rho_cs.csv')
        times = self.col.get_times_mcmc()
        dftime = pd.DataFrame(times)
        dftime.to_csv(f'{self.path_point}/res_time_MCMC.csv')
        depths = self.col.get_depths_mcmc()
        dfdep = pd.DataFrame(depths)
        dfdep.to_csv(f'{self.path_point}/res_depths_MCMC.csv')
        for quantile in self.compdlg.list_quantile :
            quantt = self.col.get_temps_quantile(quantile)
            dfquantt = pd.DataFrame(quantt)
            dfquantt.to_csv(f'{self.path_point}/res_temps_{quantile*100}.csv')
            #quantf = self.col.get_flows_quantile(quantile)
            #dfquantf = pd.DataFrame(quantf)
            #dfquantf.to_csv(f'{self.path_point}/res_flows_{quantile*100}.csv')
            #for param in ['moinslog10K','lambda_s','n', 'rho_cs'] : 
                #df = pd.DataFrame(self.col.get_moinslog10K_quantile(quantile))
                #df.to_csv(f'{self.path_point}/res_{param}_{quantile*100}.csv')
            

    def string_to_date (self, str) :
        return(datetime.strptime(str,"%Y/%m/%d %H:%M:%S"))
        

    def create_dicParam(self) :
        riv_bed = None
        depth_sensors = None
        offset = None
        dH_measures = None
        T_measures = []
        sigma_meas_P = None
        sigma_meas_T = None
        #riv_bed
        file = open(self.point.info,"r")
        lines = file.readlines()
        for line in lines:
            if line.split(';')[0].strip() == "River_Bed":
                riv_bed = float(line.split(';')[1].strip())
            if line.split(';')[0].strip() == "Delta_h":
                offset = float(line.split(';')[1].strip())
        #depth_sensors
        shaft = self.point.shaft
        item_shafts = self.sensorModel.item(2)
        shaft_sensor = None
        for row in range(item_shafts.rowCount()):
            if item_shafts.child(row).text() == shaft :
                shaft_sensor = item_shafts.child(row).data(QtCore.Qt.UserRole)
        depth_sensors = shaft_sensor.sensors_depth
        temp = shaft_sensor.t_sensor_name
        #dH_measures 
        dfp = self.dataPressure
        change_date = np.vectorize(self.string_to_date)
        dfp['Date']= change_date(dfp['Date'])
        dH_measures = list(zip(dfp['Date'].tolist(),list(zip(dfp['Pressure'].tolist(), dfp['Temperature'].tolist()))))
        #T_measures
        dft = self.dataTemperature
        dft['Date']= change_date(dft['Date'])
        T_measures = list(zip(dft['Date'].tolist(),list(zip(dft['T sensor 1'].tolist(),dft['T sensor 2'].tolist(),dft['T sensor 3'].tolist(),dft['T sensor 4'].tolist()))))
        #sigma_meas_P
        pres = self.point.pressure_sensor
        item_pres = self.sensorModel.item(0)
        pres_sensor = None
        for row in range(item_pres.rowCount()):
            if item_pres.child(row).text() == pres :
                pres_sensor = item_pres.child(row).data(QtCore.Qt.UserRole)
        sigma_meas_P = pres_sensor.sigma
        #sigma_meas_T
        item_temp = self.sensorModel.item(1)
        temp_sensor = None
        for row in range(item_temp.rowCount()):
            if item_temp.child(row).text() == temp :
                temp_sensor = item_temp.child(row).data(QtCore.Qt.UserRole)
        sigma_meas_T = temp_sensor.sigma
        dic = {'river_bed': riv_bed, 'depth_sensors' : depth_sensors, 'offset' : offset, 'dH_measures' : dH_measures, 
                'T_measures' : T_measures, 'sigma_meas_T' : sigma_meas_T, 'sigma_meas_P' : sigma_meas_P }
        return dic

    def create_computeSolveTransi(self) :
        moinslog10K = self.compdlg.doubleSpinBox_Permeability.value()
        lambda_s = self.compdlg.doubleSpinBox_Lambdas.value()
        n = self.compdlg.doubleSpinBox_Porosity.value()
        rhos_cs = self.compdlg.doubleSpinBox_ThermalCapacity.value()
        nb_cel = self.compdlg.lineEdit_CellsNumber.text()
        tuple = ((float(moinslog10K), float(lambda_s), float(n), float(rhos_cs)), int(float(nb_cel)))
        return tuple

    def create_paramMCMC(self) : 
        range_moinslog10K_min = float(self.compdlg.doubleSpinBox_PermeabilityMin.value())
        range_moinslog10K_max = float(self.compdlg.doubleSpinBox_PermeabilityMax.value())
        sigma_moinslog10K = float(self.compdlg.doubleSpinBox_PermeabilitySigma.value())

        range_lambda_s_min = float(self.compdlg.doubleSpinBox_LambdasMin.value())
        range_lambda_s_max = float(self.compdlg.doubleSpinBox_LambdasMax.value())
        sigma_lambda_s = float(self.compdlg.doubleSpinBox_LambdasSigma.value())

        range_n_min = float(self.compdlg.doubleSpinBox_PorosityMin.value())
        range_n_max = float(self.compdlg.doubleSpinBox_PorosityMax.value())
        sigma_n = float(self.compdlg.doubleSpinBox_PorositySigma.value())

        range_rhos_cs_min = float(self.compdlg.doubleSpinBox_ThermalCapacityMin.value())
        range_rhos_cs_max = float(self.compdlg.doubleSpinBox_ThermalCapacityMax.value())
        sigma_rhos_cs = float(self.compdlg.doubleSpinBox_ThermalCapacitySigma.value())

        priors = {'moinslog10K' : ((range_moinslog10K_min, range_moinslog10K_max), sigma_moinslog10K), 'lambda_s' : ((range_lambda_s_min, range_lambda_s_max), sigma_lambda_s), 'n' : ((range_n_min, range_n_max), sigma_n), 'rhos_cs' : ((range_rhos_cs_min, range_rhos_cs_max), sigma_rhos_cs)}

        nb_iter = int(float(self.compdlg.lineEdit_IterationsNumber.text()))
        nb_cel = int(float(self.compdlg.lineEdit_CellsNumberMCMC.text()))

        quantile = self.compdlg.list_quantile

        tuple = (priors, nb_iter, nb_cel, quantile)

        return tuple






        


    

    

   
