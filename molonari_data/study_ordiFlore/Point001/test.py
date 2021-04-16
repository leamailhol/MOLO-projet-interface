#Remove 15 first measurements
#dft = dft.iloc[15:]
#dfp = dfp.iloc[15:]
#Remove Spurious Temperatures (Kelvin)
#dft.iloc[:,2:]=np.where((dft.iloc[:,2:]<274), np.NaN, dft.iloc[:,2:])
#dft.iloc[:,2:]=np.where((dft.iloc[:,2:]>304,), np.NaN, dft.iloc[:,2:])
#Remove Spurious Head Differential (Meters)
#dfp.iloc[:,2:]=np.where((dfp.iloc[:,2:]>0.1), np.NaN, dfp.iloc[:,2:])
#dfp.iloc[:,2:]=np.where((dfp.iloc[:,2:]<-0.1,), np.NaN, dfp.iloc[:,2:])
print("coucou")