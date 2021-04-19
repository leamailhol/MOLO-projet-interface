#Remove 15 first measurements
#dft = dft.iloc[15:]
#dfp = dfp.iloc[15:]
#Remove Spurious Temperatures (Kelvin)
dft.iloc[:,4:]=np.where((dft.iloc[:,4:]<274), np.NaN, dft.iloc[:,4:])
dft.iloc[:,4:]=np.where((dft.iloc[:,4:]>304), np.NaN, dft.iloc[:,4:])
#Remove Spurious Head Differential (Meters)
dfp.iloc[:,4:]=np.where((dfp.iloc[:,4:]>0.1), np.NaN, dfp.iloc[:,4:])
dfp.iloc[:,4:]=np.where((dfp.iloc[:,4:]<-0.1), np.NaN, dfp.iloc[:,4:])
print("coucou")