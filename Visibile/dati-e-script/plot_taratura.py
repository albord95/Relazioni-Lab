"""plot taratura duplicatore di frequenza"""

from pylab import *

grad1, Vpp1, dVpp1 = loadtxt('borcapVLTvsAng01.txt', unpack= True)
grad2, Vpp2, dVpp2 = loadtxt('borcapVLTvsAng02.txt', unpack= True)
tgrad, tpower = loadtxt('borcapVLtaratura01.txt', unpack= True)

'''grad = concatenate((grad2, grad1))
Vpp = concatenate((Vpp2, Vpp1))
dVpp = concatenate((dVpp2, dVpp1))
grad = grad[argsort(grad)]
Vpp = Vpp[argsort(grad)]
dVpp = dVpp[argsort(grad)]'''

power1 = zeros(len(Vpp1))
for i in range(len(power1)):
    for j in range(len(tpower)):
        if grad1[i] == tgrad[j]:
            power1[i] = tpower[j]
            break

power2 = zeros(len(Vpp2))
for i in range(len(power2)):
    for j in range(len(tpower)):
        if grad2[i] == tgrad[j]:
            power2[i] = tpower[j]
            break

dpower1 = power1*0.03
    
dy = 0.68*0.5*dVpp 
dx = dpower

figure(1).set_tight_layout(True)
clf()
errorbar(power1, Vpp1, fmt='.', yerr=dVpp1, xerr=power1*0.03, markersize=4)
errorbar(power2, Vpp2, fmt='.', yerr=dVpp2, xerr=power2*0.03, markersize=4)
xlim(0, 1.05*max(power1))
ylabel('intensità [mV]')
xlabel('potenza [mW]')

figure(2).set_tight_layout(True)
clf()
errorbar(arange(len(tgrad)), tpower, fmt='.', yerr=tpower*0.03, elinewidth=2, label='errore di calibrazione (3%)', markersize=3)
#errorbar(arange(len(prettygrad)), prettypower, fmt='.k', yerr=prettypower*0.01, elinewidth=3, markersize=7, label='errore statistico (1%)')
xlabel('angolo [grad]', fontsize='large')
ylabel('potenza [mW]', fontsize='large')
xticks(arange(len(tgrad)), tgrad.astype(int), rotation=70, fontsize='x-small')
legend(fontsize='x-large')

'''derivataseconda = diff(diff(tpower))
figure(3).set_tight_layout(True)
clf()
plot(derivataseconda)
xlabel('angolo [grad]', fontsize='large')
ylabel('derivata discreta della potenza [mW]', fontsize='large')
ylim(-46, 25)
xticks(arange(len(tgrad)), grad.astype(int), rotation=60, fontsize='small')

indicibuoni = []
for i in range(len(derivataseconda)):
    if abs(derivataseconda[i]) < 50:
        indicibuoni.append(i)
indicubuoni = array(indicibuoni)

figure(4).set_tight_layout(True)
clf()
plot(derivataseconda[indicibuoni])
xticks(arange(len(tgrad[indicibuoni])), tgrad[indicibuoni].astype(int), rotation=60, fontsize='small')

buoni = derivataseconda[indicibuoni]
stdmobile = []
for i in range(len(buoni)-10):
    stdmobile.append(buoni[i:i+10].std())
    
figure(5)
clf()
plot(stdmobile)'''
    