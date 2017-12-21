from pylab import *

filename = 'borcapasv09.txt'

##cambio virgole in punti del file che voglio importare
f = open(filename,'r')
filedata = f.read()
f.close()
newdata = filedata.replace(",",".")
f = open(filename,'w')
f.write(newdata)
f.close()

t, vmax, vmin , t2, rampamax, rampamin = loadtxt(filename, comments='"', unpack=True)

figure(1).set_tight_layout(True)
clf()
plot(1000*t, 1000*vmax) #ms, mV
plot(1000*t, 1000*vmin) #ms, mV
grid()
xlim(min(1000*t), max(1000*t))
xlabel('t [ms]')
ylabel('segnale della trasmittività [mV]')