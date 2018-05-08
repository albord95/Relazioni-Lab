from pylab import *
from lab import fit_curve, xe

files = ['borcapVMspettro01.txt',
         'borcapVMspettro03_550.txt',
         'borcapVMspettro07_823_300ms.txt',
         'borcapVMspettro08_668_30ms.txt',
         'borcapVMspettro09_551_9ms.txt',
         'borcapVMspettro10_551_290ms.txt']

l_fondo1, a_fondo1 = loadtxt('borcapVMspettro02fondo.txt', unpack=True)
l_fondo2, a_fondo2 = loadtxt('borcapVMspettro06fondo.txt', unpack=True)
l1, a1 = loadtxt('borcapVMspettro04_550.txt', unpack=True)

figure(1).set_tight_layout(True)
clf()
figure(2).set_tight_layout(True)
clf()
figure(3).set_tight_layout(True)
clf()


altezza = 3
larghezza = 2

for i in range(len(files)):
    filename= files[i]
    l, a = loadtxt(filename, unpack=True)
    figure(1)
    subplot(altezza, larghezza, i+1)
    plot(l, a)
    if i%2 == 0:
        ylabel('segnale [a.u.]')
    if i >= 4:
        xlabel('$\lambda$ [nm]')
    
figure(2)
subplot(2, 1, 1)
plot(l_fondo1, a_fondo1)
ylabel('segnale [a.u.]')
subplot(2, 1, 2)
plot(l_fondo2, a_fondo2)
ylabel('segnale [a.u.]')
xlabel('$\lambda$ [nm]')

figure(3)
plot(l1, a1)
ylabel('segnale [a.u.]')
xlabel('$\lambda$ [nm]')
