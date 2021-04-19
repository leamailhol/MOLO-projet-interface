import os 
import pandas as pd 
import matplotlib.pyplot as plt



path = 'D:/Documents/Cours/2A/Molonari/Interface/MOLO-projet-interface/molonari_data/study_ordiMaëlle/Point001'
os.chdir(path)

dataT = pd.read_csv('processed_temperature.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
dataT.describe()
dataT.head()

dataP = pd.read_csv('processed_pressure.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
dataP.describe()
print(dataP)

#plt.plot(dataT['Date'], dataT['T sensor 1'])

plt.plot(dataP['Date'], dataP['Pressure'])


plt.show()

