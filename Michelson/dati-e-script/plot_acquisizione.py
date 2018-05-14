from pylab import *
from glob import glob

#files = glob('borcapMM*')

files = ['borcapMM01.txt', 'borcapMM02.txt', 'borcapMM03.txt', 'borcapMM04.txt', 'borcapMM05.txt', 'borcapMM06.txt', 'borcapMM07.txt', 'borcapMM08.txt', 'borcapMM09.txt', 'borcapMM10.txt' ]

#for i in range(len(files)):
#    figure(i)
#    clf()
#    t, V = loadtxt(files[i], unpack = True)
#    plot(t, V)
    
figure(1).set_tight_layout(True)
clf()
t, V = loadtxt(files[5], unpack = True)
plot(t, V)
xlim(500,517)
ylim(1,3.8)
xlabel('tempo [s]')
ylabel('tensione [V]')
savefig('esempio_acquisizione.pdf')

