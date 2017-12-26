"""script che calcola l'offset"""

from pylab import *
from statistics import mode

numeri0 = ['02','03','04','05','06','07','08','09','10','11','12','13','14','15','16']
numeri1 = ['02a','02b','02c','03a','03b','03c','04a','04b','04c','05a','05b','05c','06a', '06b','06c','07a','07b','07c','08a','08b','08c','09a','09b','09c','10a','10b','11a', '11b','12a','13a','13b','14a','14b','15a','15b','16a','16b']
numeri = numeri0 + numeri1
files = ['borcapasv00.txt']*len(numeri)
for j in range(len(files)):
    files[j] = 'borcapasv' + numeri[j] + '.txt'
    
for i in range(len(files)):
    filename = files[i]
    f = open(filename,'r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace(",",".")
    f = open(filename,'w')
    f.write(newdata)
    f.close()
    t, volt1, volt2, _, rampa1, rampa2 = loadtxt(filename, comments='"', unpack=True)
    volt = (volt1 + volt2) / 2
    volt = volt*1000 #mV
    print(numeri[i], mode(volt))
