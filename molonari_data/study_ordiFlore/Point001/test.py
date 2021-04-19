#Remove 15 first measurements
#dft = dft.iloc[15:]
#dfp = dfp.iloc[15:]
#Remove Spurious Temperatures (Kelvin)
dft.iloc[:,3:]=np.where((dft.iloc[:,3:]<274), np.NaN, dft.iloc[:,3:])
dft.iloc[:,3:]=np.where((dft.iloc[:,3:]>304), np.NaN, dft.iloc[:,3:])
#Remove Spurious Head Differential (Meters)
dfp.iloc[:,3:]=np.where((dfp.iloc[:,3:]>0.1), np.NaN, dfp.iloc[:,3:])
dfp.iloc[:,3:]=np.where((dfp.iloc[:,3:]<-0.1), np.NaN, dfp.iloc[:,3:])
print("coucou")