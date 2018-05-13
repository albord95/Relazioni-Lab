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
l1, a1 = loadtxt('borcapVMspettro10_551_290ms.txt', unpack=True)

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
x = ones(4500)*800
x1 = ones(4500)*670
x2 = ones(4500)*850
y = linspace(0, 4500, 4500)
plot(x, y, color = 'tab:pink', label='$\lambda$ = 800 nm')
plot(x1, y, color = 'tab:red', label='$\lambda$ = 670 nm')
plot(x2, y, color = 'm', label='$\lambda$ = 850 nm')
plot(l1, a1)
ylabel('segnale [a.u.]')
xlabel('$\lambda$ [nm]')
ylim(0, 4500)
legend()
